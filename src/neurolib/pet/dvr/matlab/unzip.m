function result = unzip(zipped_file, output_file)

  if ~exist(zipped_file)
      error("Zipped file does not exist: %s", zipped_file)
  end

  [dir basename suffix] = fileparts(zipped_file);

  assert(strcmp(suffix, '.gz'));

  result = system(['gunzip --stdout ' zipped_file ' > ' output_file]);
