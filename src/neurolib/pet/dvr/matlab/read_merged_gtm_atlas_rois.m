function result = read_merged_gtm_atlas_rois()
%  46x2 cell array
%
%  {'Accumbens_area_bh'          }    {1x2 double}
%  {'Amygdala_bh'                }    {1x2 double}
%  ...


rois = read_gtm_atlas_rois();

tmp = regexprep(rois.names,'(_lh|_rh)',''); % consecutive duplicated names
[k1,k2,k3] = unique(tmp,'stable'); % k3 100: 1 1 2 3 3 4 5 6 7 7 ...
list = unique(k3,'stable'); % 1 2 3 4 ... uniques in order
result = {};
for ii = list(:)'  % 1 2 3 .. 54
  i1 = find(k3==ii); % [1 2]
  if numel(i1)>1
    result{end+1,1} = regexprep(rois.names{i1(1)},'(_lh|_rh)','_bh');
    result{end,2} = (i1');
  end
end
