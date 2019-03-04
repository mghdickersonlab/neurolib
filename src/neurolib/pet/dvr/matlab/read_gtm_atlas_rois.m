function result = read_gtm_atlas_rois()
    gtm_atlas_labels_file = [fileparts(mfilename('fullpath')) filesep 'gtmatlaslabels2.txt'];
    labels = ReadInFile(gtm_atlas_labels_file, ' ', 1);
    [tr i] = sort(labels(:,3));
    tmp = labels(i,:);

    result.indices = cell2mat(tmp(:,1));
    result.lut_indices = cell2mat(tmp(:,2));
    result.names = tmp(:,3);


