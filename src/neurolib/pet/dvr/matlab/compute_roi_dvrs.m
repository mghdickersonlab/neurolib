function result = compute_roi_dvrs(gtmpvc_dir, frame_times_file, time_window_start_end, ref_roi, weighted_merge, output_csv)

  gtm_file = [gtmpvc_dir filesep 'gtm.nii'];
  seg_file = [gtmpvc_dir filesep 'aux' filesep 'seg.nii'];
  gtm_file_gz = [gtm_file '.gz'];
  seg_file_gz = [seg_file '.gz'];

  unzip([gtm_file '.gz'], gtm_file);
  unzip([seg_file '.gz'], seg_file);

  frame_start_times_and_durations = read_frame_times(frame_times_file);
  frame_start_times = frame_start_times_and_durations(:,1);

  if ~exist(fileparts(output_csv),'dir'); mkdir(fileparts(output_csv)); end

  tac = read_gtm_tacs(gtm_file, seg_file, weighted_merge);

  ref_roi_int_index = searchCellStr(['^' ref_roi '$'], tac.roi_names);

  refsig  = tac.tacs(:, ref_roi_int_index);
  regint = cumtrapz(frame_start_times, tac.tacs) ./ tac.tacs;
  refint = cumtrapz(frame_start_times, refsig);

  REF = repmat(refint,1,size(tac.tacs, 2)) ./ tac.tacs;

  time_window_indices = find(frame_start_times >= time_window_start_end(1) & ...
                              frame_start_times < time_window_start_end(2));
  S1 = demean(regint(time_window_indices,:));
  S2 = demean(REF(time_window_indices,:));
  CV = LoopCross(S1,S2);
  V2 = LoopCross(S2,S2);
  slope = CV./V2;

  csv_table = [];
  csv_table.regionname = tac.roi_names;
  csv_table.Nvox = tac.num_voxels;
  csv_table.DVR_PVC = slope(:);
  csv_table = struct2table(csv_table);
  [tr i] = sort(csv_table.regionname);
  csv_table = csv_table(i,:);

  writetable(csv_table, output_csv);
end
