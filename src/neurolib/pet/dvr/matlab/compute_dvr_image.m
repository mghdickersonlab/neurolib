function result = compute_dvr_image(pet_file, gtmpvc_dir, frame_times_file, time_window_start_end, ref_roi, weighted_merge, outimage)

  unzipped_pet_file = pet_file;
  [dir basename suffix] = fileparts(pet_file);
  temp_unzipped = 0;
  if strcmp(suffix, '.gz')
    unzipped_pet_file = [dir filesep basename];
    unzip(pet_file, unzipped_pet_file);
    temp_unzipped = 1;
  end

  gtm_file = [gtmpvc_dir filesep 'gtm.nii'];
  seg_file = [gtmpvc_dir filesep 'aux' filesep 'seg.nii'];

  unzip([gtm_file '.gz'], gtm_file);
  unzip([seg_file '.gz'], seg_file);

  frame_start_times_and_durations = read_frame_times(frame_times_file);
  frame_start_times = frame_start_times_and_durations(:,1);

  time_window_indices = find(frame_start_times >= time_window_start_end(1) & ...
                             frame_start_times < time_window_start_end(2));

  tac = read_gtm_tacs(gtm_file, seg_file, weighted_merge);
  ref_roi_int_index = searchCellStr(['^' ref_roi '$'], tac.roi_names);
  refsig  = tac.tacs(:, ref_roi_int_index);

  pet_2d = ReadAndSmooth(unzipped_pet_file,[2 2 2],[]);
  regint = cumtrapz(frame_start_times, pet_2d) ./ pet_2d;
  refint = cumtrapz(frame_start_times, refsig);
  REF = repmat(refint,1,size(pet_2d,2))./pet_2d;

  S1 = demean(regint(time_window_indices,:));
  S2 = demean(REF(time_window_indices,:));

  CV = LoopCross(S1,S2);
  V2 = LoopCross(S2,S2);

  slope = CV./V2;
  slope(isnan(slope))=0;

  pet_vol_frame1 = spm_vol([unzipped_pet_file ',1']);
  hdr = pet_vol_frame1(1);
  vol = zeros(hdr.dim);
  vol(:) = slope;
  hdr.pinfo(1) = 1;
  hdr.dt = [16 0];
  hdr.fname = outimage;
  description = ['Reference ROI: ' ref_roi ';  Time: ' regexprep(num2str(round(time_window_start_end)),'  ','-')];
  hdr.descrip = description;
  spm_write_vol(hdr, vol);

  if temp_unzipped
    system(['rm ' unzipped_pet_file])
  end

  [dir basename suffix] = fileparts(outimage);
  if strcmp(suffix, '.gz')
    unzipped_pet_file = [dir filesep basename]
    unzip(pet_file, unzipped_pet_file)
    temp_unzipped = 1
  end

  system(['rm ' gtm_file]);
  system(['rm ' seg_file]);
