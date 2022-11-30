# from Yangwang1.base import logging_tools
from SKA_pipeline.base import logging_tools_for_mutilprocess as logging_tools
from os import path
import pandas as pd
import numpy as np
# from pandas.util import hash_pandas_object
import time
from astropy.io import fits
from astropy.wcs import WCS

class PipelinePort(object):
    def __init__(self, file, *args, **kwargs):
        """
        Base class defining functionality for all pipeline stages. To
        contribute a new pipeline stage to yangwang, create a new class and
        inherit PipelinePort. Always start by calling "super().__init__()" and
        pass it all the arguments of the init function in your new class. The
        only other function that needs to be changed is `_execute_function`
        which should actually implement pipeline stage functionality. The base
        class will take care of automatic logging, deciding whether or not a
        function has already been run on this data, saving and loading of files
        and error checking of inputs and outputs.

        Parteamers-
        ---------
        force_rerun : bool
            If True will force the function to run over all data, even if it
            has been called before.
        save_output : bool
            If False will not save and load any files. Only use this if
            functions are very fast to rerun or if you cannot write to disk.
        output_dir : string
            Output directory where all outputs will be stored. Defaults to
            current working directory.
        file_format : string
            Format to save the output of this pipeline stage to.
            Accepted values are:
            parquet
        # drop_nans : bool
        #     If true, will drop any NaNs from the input before passing it to the
        #     function

        """

        # This will be the name of the child class, not the parent.
        self.class_name = type(locals()['self']).__name__
        self.file = file
        self.function_call_signature = \
            logging_tools.format_function_call(self.class_name, self.file, **kwargs)

        if 'input_dir' in kwargs:
            self.input_dir = kwargs['input_dir']

        # Disables the automatic saving of intermediate outputs
        if 'save_output' in kwargs and kwargs['save_output'] is False:
            self.save_output = False
        else:
            self.save_output = True

        # Handles automatic file reading and writing
        if 'output_dir' in kwargs:
            self.output_dir = kwargs['output_dir']
        else:
            self.output_dir = './'

        if 'log_dir' in kwargs:
            self.log_dir = kwargs['log_dir']
        else:
            self.log_dir = '/home/lab30201/sdd/slc/SKAData/SKA_algorithm/SKA_pipeline/datas/TemporaryData'

        # This allows the automatic logging every time this class is
        # instantiated (i.e. every time this pipeline stage
        # is run). That means any class that inherits from this base class
        # will have automated logging.

        if 'queue' in kwargs:
            self.queue = kwargs['queue']
            # multiprocess log configure
            # logging_tools.worker_configurer(self.queue)
        else:
            # single process log configure
            logging_tools.setup_logger(log_directory=self.log_dir,
                                       log_filename='SH.log')

        if 'force_rerun' in kwargs and kwargs['force_rerun']:
            self.args_same = False
        else:
            self.args_same = \
                logging_tools.check_if_inputs_same(self.class_name, self.file, 
                                                   locals()['kwargs'])

        if 'file_format' in kwargs:
            self.file_format = kwargs['file_format']
        else:
            self.file_format = 'npy'

        if 'exposure_infor' in kwargs:
            self.exposure_infor = kwargs['exposure_infor']
        else:
            pass

        # try:
        #     self.exposure_infor = kwargs['exposure_infor']
        # except AttributeError:
        #     print("No exposure time information!!!")

        if isinstance(self.file, list):
            self.file_name = [path.basename(each).split(".fit")[0] for each in self.file]
            self.output_file = [path.join(self.output_dir, each + '.%s' % self.file_format) for each in self.file_name]
        else:
            self.file_name = path.basename(self.file).split(".fit")[0]
            self.output_file = path.join(self.output_dir, self.file_name + '.%s' % self.file_format)

    def save(self, output, filename, file_format=''):
        """
        Saves the output of this pipeline stage.

        Parameters
        ----------
        output : pd.DataFrame
            Whatever the output is of this stage.
        filename : str
            File name of the output file.
        file_format : str, optional
            File format can be provided to override the class's file format
        """
        if len(file_format) == 0:
            file_format = self.file_format

        if self.save_output:
            # Parquet needs strings as column names
            # (which is good practice anyway)
            # output.columns = output.columns.astype('str')
            if file_format == 'parquet':
                output.columns = output.columns.astype('str')
                if '.parquet' not in filename:
                    filename += '.parquet'
                output.to_parquet(filename)

            elif file_format == 'csv':
                # output.columns = output.columns.astype('str')
                if '.csv' not in filename:
                    filename += '.csv'
                output.to_csv(filename)

            elif file_format == 'npy':
                if '.npy' not in filename:
                    filename += '.npy'
                # output.to_csv(filename)
                np.save(filename, output)

            elif file_format == 'fits':
                if '.fits' not in filename:
                    filename += '.fits'
                hdu = fits.HDUList([fits.PrimaryHDU(output)])
                hdu.writeto(filename, overwrite=True)
                hdu.close()

            elif file_format == 'fit':
                if '.fit' not in filename:
                    filename += '.fit'
                hdu = fits.HDUList([fits.PrimaryHDU(output)])
                hdu.writeto(filename, overwrite=True)
                hdu.close()

            elif file_format == 'list' or file_format == 'txt':
                if '.%s' % file_format not in filename:
                    filename += '.%s' % file_format
                with open(filename, 'w') as f:
                    f.write(output)

    def load(self, filename, file_format=''):
        """
        Loads previous output of this pipeline stage.

        Parameters
        ----------
        filename : str
            File name of the output file.
        file_format : str, optional
            File format can be provided to override the class's file format

        Returns
        -------
        output : pd.DataFrame
            Whatever the output is of this stage.
        """
        if len(file_format) == 0:
            file_format = self.file_format

        if file_format == 'parquet':
            if '.parquet' not in filename:
                filename += '.parquet'
            output = pd.read_parquet(filename)
        elif file_format == 'csv':
            if '.csv' not in filename:
                filename += '.csv'
            output = pd.read_csv(filename)
        elif file_format == 'npy':
            if '.npy' not in filename:
                filename += '.npy'
            output = np.load(filename)
        elif file_format == 'fits':
            if '.fits' not in filename:
                filename += '.fits'
            with fits.open(filename) as hdu:
                output = hdu[0].data
                wcs = WCS(hdu[0].header)
                return output,wcs
        elif file_format == 'fit':
            if '.fit' not in filename:
                filename += '.fit'
            with fits.open(filename) as hdu:
                output = hdu[0].data
        elif file_format == 'list' or file_format == 'txt':
            if '.%s' % file_format not in filename:
                filename += '.%s' % file_format
            with open(filename, 'r') as f:
                output = f.readlines()
        return output

    def run(self, previous_stage_output):
    # def run(self):
        """
        This is the external-facing function that should always be called
        (rather than _execute_function). This function will automatically check
        if this stage has already been run with the same arguments and on the
        same data. This can allow a much faster user experience avoiding
        rerunning functions unnecessarily.

        Parameters
        ----------
        file : str
            Input file on which to run this pipeline stage on.

        Returns
        -------
        pd.DataFrame
            Output
        """
        # new_checksum = self.hash_data(data)
        # if '.%s' % self.file_format not in output_file:
        # 	output_file += '.%s' % self.file_format

        # if self.force_rerun is False and path.exists(self.output_file):
        if self.args_same and path.exists(self.output_file):
        # if self.args_same and new_checksum == self.checksum:
            # This means we've already run this function for all instances in
            # the input and with the same arguments
            msg = "Pipeline stage %s previously called on %s. " \
                  "Use 'force_rerun=True' in init args to override this " \
                  "behavior." % (self.class_name, path.basename(self.file))
            # logging_tools.log(msg, level='WARNING')
            if "queue" in locals().keys():
                logging_tools.log_for_queue(msg, self.queue, level='WARNING')
            else:
                logging_tools.log(msg, level='WARNING')
            print("*****now skip!!")
            return self.output_file
            # return self.file_name
            # return self.previous_output
        else:
            # msg_string = self.function_call_signature + ' - checksum: ' + \
            #     (str)(new_checksum)
            # print(msg_string)
            print('Running', self.class_name, '...')
            t1 = time.time()

            output = self._execute_function(previous_stage_output)
            # self.save(output, self.output_file)
            taken_time = time.time() - t1
            print('Done! Time taken: %d s' % taken_time)
            msg_string = self.function_call_signature + " - Run Time: %d s" % round(taken_time, 2)
            # logging_tools.log(msg_string)
            # logging_tools.log_for_queue(msg_string, self.queue)
            if "queue" in locals().keys():
                logging_tools.log_for_queue(msg_string, self.queue)
            else:
                logging_tools.log(msg_string)
            return output

    def run_on_dataset(self, previous_stage_output):
        """
        This is the external-facing function that should always be called
        (rather than _execute_function). This function will automatically check
        if this stage has already been run with the same arguments and on the
        same data. This can allow a much faster user experience avoiding
        rerunning functions unnecessarily.

        Parameters
        ----------
        file : str
            Input file on which to run this pipeline stage on.

        Returns
        -------
        pd.DataFrame
            Output
        """
        # new_checksum = self.hash_data(data)
        # if '.%s' % self.file_format not in output_file:
        # 	output_file += '.%s' % self.file_format
        if self.args_same and (False not in [path.exists(x) for x in self.output_file]):
            msg = "Pipeline stage %s previously called on %s. " \
                  "Use 'force_rerun=True' in init args to override this " \
                  "behavior." % (self.class_name, [path.basename(each) for each in self.file])
            # logging_tools.log(msg, level='WARNING')
            # logging_tools.log_for_queue(msg, self.queue, level='WARNING')
            if "queue" in locals().keys():
                logging_tools.log_for_queue(msg, self.queue, level='WARNING')
            else:
                logging_tools.log(msg, level='WARNING')
            print("*****now skip!!")
            return self.output_file

        elif not self.args_same or (True not in [path.exists(x) for x in self.output_file]):
            print('Running', self.class_name, '...')
            t1 = time.time()

            output = self._execute_function(previous_stage_output)
            # self.save(output, self.output_file)
            taken_time = time.time() - t1
            print('Done! Time taken: %d s' % taken_time)
            msg_string = self.function_call_signature + " - Run Time: %d s" % round(taken_time, 2)
            # logging_tools.log(msg_string)
            # logging_tools.log_for_queue(msg_string, self.queue)
            if "queue" in locals().keys():
                logging_tools.log_for_queue(msg_string, self.queue)
            else:
                logging_tools.log(msg_string)
            return output

        else:
            # processed, unprocessed = [], []
            unprocessed = []
            for index, i in enumerate(self.output_file):
                if path.exists(i):
                    # processed.append(i)
                    msg = "Pipeline stage %s previously called on %s. " \
                          "Use 'force_rerun=True' in init args to override this " \
                          "behavior." % (self.class_name, path.basename(self.file[index]))
                    # logging_tools.log(msg, level='WARNING')
                    # logging_tools.log_for_queue(msg, self.queue, level='WARNING')
                    if "queue" in locals().keys():
                        logging_tools.log_for_queue(msg, self.queue, level='WARNING')
                    else:
                        logging_tools.log(msg, level='WARNING')
                    print("*****now skip!!")
                else:
                    unprocessed.append(previous_stage_output[index])

            if len(unprocessed) != 0:
                # msg_string = self.function_call_signature + ' - checksum: ' + \
                #     (str)(new_checksum)
                # print(msg_string)
                print('Running', self.class_name, '...')
                t1 = time.time()

                output = self._execute_function(unprocessed)
                # self.save(output, self.output_file)
                taken_time = time.time() - t1
                print('Done! Time taken: %d s' % taken_time)
                msg_string = self.function_call_signature + " - Run Time: %d s" % round(taken_time, 2)
                # logging_tools.log(msg_string)
                # logging_tools.log_for_queue(msg_string, self.queue)
                if "queue" in locals().keys():
                    logging_tools.log_for_queue(msg_string, self.queue)
                else:
                    logging_tools.log(msg_string)
            return self.output_file

    # def _execute_function(self, data):
    def _execute_function(self, previous_stage_output):
        """
        This is the main function of the PipelinePort and is what should be
        implemented when inheriting from this class.

        Parameters
        ----------
        data : Dataset object, pd.DataFrame
            Data type depends on whether this is feature extraction stage (so
            runs on a Dataset) or any other stage (e.g. anomaly detection)

        Raises
        ------
        NotImplementedError
            This function must be implemented when inheriting this class.
        """
        raise NotImplementedError
