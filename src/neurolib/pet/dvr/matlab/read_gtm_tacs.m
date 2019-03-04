function result = read_gtm_tacs(gtm_file, atlas, weighted_merge)

  roi = read_gtm_atlas_rois();
  merged_rois = read_merged_gtm_atlas_rois();

  tacs = FastRead(gtm_file);
  tacs = tacs(:, roi.indices);

  seg = FastRead(atlas);
  num_voxels = [];
  for ii = 1:size(roi.lut_indices, 1)
    vol_indices = find(seg(:) == roi.lut_indices(ii));
    num_voxels(ii,1) = numel(vol_indices);
  end

  roi_names_with_merged = roi.names;

  % Add TAC for each merged ROI
  for ii = 1:size(merged_rois,1)
    merged_roi_name = merged_rois{ii, 1};
    hemi_indices = merged_rois{ii, 2};
    if weighted_merge
      tacs(:,end+1) = sum(tacs(:, hemi_indices).*repmat(num_voxels(hemi_indices)',size(tacs,1),1),2)./ ...
                         sum(repmat(num_voxels(hemi_indices)',size(tacs,1),1),2);
    else
      tacs(:,end+1) = mean(tacs(:, hemi_indices), 2);
    end
    roi_names_with_merged{end+1,1} = merged_roi_name;
    num_voxels(end+1,1) = sum(num_voxels(hemi_indices));
  end

  result = [];
  result.tacs = tacs;
  result.roi_names = roi_names_with_merged;
  result.num_voxels = num_voxels;
