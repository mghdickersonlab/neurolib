function dat = ReadAndSmooth(P,s,prefix)
% 3 dimensional convolution of an image
% FORMAT spm_smooth(P,Q,S,dtype)
% P     - image to be smoothed (or 3D array)
% Q     - filename for smoothed image (or 3D array)
% S     - [sx sy sz] Gaussian filter width {FWHM} in mm (or edges)
% dtype - datatype [default: 0 == same datatype as P]
%____________________________________________________________________________
%
% spm_smooth is used to smooth or convolve images in a file (maybe).
%
% The sum of kernel coeficients are set to unity.  Boundary
% conditions assume data does not exist outside the image in z (i.e.
% the kernel is truncated in z at the boundaries of the image space). S
% can be a vector of 3 FWHM values that specifiy an anisotropic
% smoothing.  If S is a scalar isotropic smoothing is implemented.
%
% If Q is not a string, it is used as the destination of the smoothed
% image.  It must already be defined with the same number of elements
% as the image.
%
%_______________________________________________________________________
% Copyright (C) 2008 Wellcome Trust Centre for Neuroimaging

% John Ashburner & Tom Nichols
% $Id: spm_smooth.m 4172 2011-01-26 12:13:29Z guillaume $

%-----------------------------------------------------------------------
P = spm_vol(char(P));
VOX = sqrt(sum(P(1).mat(1:3,1:3).^2));


% compute parameters for spm_conv_vol
%-----------------------------------------------------------------------
s  = s./VOX;                        % voxel anisotropy
s1 = s/sqrt(8*log(2));              % FWHM -> Gaussian parameter

x  = round(6*s1(1)); x = -x:x; x = spm_smoothkern(s(1),x,1); x  = x/sum(x);
y  = round(6*s1(2)); y = -y:y; y = spm_smoothkern(s(2),y,1); y  = y/sum(y);
z  = round(6*s1(3)); z = -z:z; z = spm_smoothkern(s(3),z,1); z  = z/sum(z);

i  = (length(x) - 1)/2;
j  = (length(y) - 1)/2;
k  = (length(z) - 1)/2;


k = ones(numel(x),numel(y),numel(z));
[i1 i2 i3] = ind2sub(size(k),1:numel(k));
val = prod([x(i1)' y(i2)' z(i3)'],2);
k(:) = val;

dat = zeros(numel(P),prod(P(1).dim));
for ii = 1:numel(P);
    m = spm_read_vols(P(ii));
    m(isnan(m))=0;
    nm = convn(m,k,'same');
    dat(ii,:) = nm(:)';
    
    if ~isempty(prefix);
        [a b c] = fileparts(P(ii).fname);
        if ~isempty(a); a = [a filesep]; end
        nfn = [a prefix b c];
        P(ii).fname = nfn;
        P(ii).dt = [16 0];
        spm_write_vol(P(ii),nm);
    end
end
% 
% %%
% m1 = openIMG('ss_PredImage.nii');
% [m2 h] = openIMG('PredImage.nii');
% h.fname = 'Test.nii';
% % m3 = convn(m2,k,'same');
% % m2(m2==0)=NaN;
% m3 = convn(m2,k,'full');
% 
% 
% m3 = m3(8:end-7,8:end-7,8:end-7);
% clc;R
% size(m2)
% size(m3)
% 
% m4 = m3;
% m3 = convn(m2,k,'same');
% 
% 
% %%
% 
% % m3 = spm_conv(m2,8/3);
% spm_write_vol(h,m3);
% m3 = openIMG('Test.nii');
% figure(20); clf; plot(m1(:),m3(:),'.'); shg
% % figure(21); clf; plot(m1(:),m2(:),'.'); shg
% tmp = (find(abs(m1(:)-m3(:))>.000001));
% m2(:) = 0;
% m2(tmp) = 1;
% h.fname = 'DiffMask.nii'
% spm_write_vol(h,m2);
