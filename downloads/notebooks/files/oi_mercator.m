% oi_mercator

% Optimally interpolate the data set x,y,data using the chosen covariance
% function form

%% Take a chunk of the data out to ilustrate what happens to the expected
%  error when the sampling is sparse  
if demo_gap
  clip = find(xx>-70&xx<-68);
  xkm(clip) = [];
  ykm(clip) = [];
  xx(clip) = [];
  yy(clip) = [];
  data(clip) = [];
end

%% Coordinate matrices
% Build matrices that repeat columns of x and rows of y. Then X-X' and Y-Y' 
% will be all possible distance combinations between pairs of points
X = repmat(xkm,[1 length(ykm)]);
Y = repmat(ykm',[length(xkm) 1]);

%% Build the data-data covariance matrix

% recall that we have the distance for every point to every other point:
Rdd = sqrt((X-X').^2+(Y-Y').^2);

% Evaluate the normalized covariance using the fitted function

% Use Markov covariance function with parameters fitted in vector 'b'
% Use normalized covariance C(0)=1 because signal variance
% cancels out in product of Cmd*inv(Cdd)

b(2) = 50;  % or 300 <---- see what happens with sub-optimal scale
disp(['optimal length scale was ' num2str(b(2))]) 
switch best_method
  case 'Markov'
    Cdd0 = (1+Rdd/b(2)).*exp(-Rdd/(b(2))); 
  case 'Gaussian'
    error([mfilename 'code is set up for Markov function case only'])
end

% Add error/signal variance to the diagonal
ssq = b(1); % signal variance is given by y-intercept from function fit
lambda = esq/ssq;
Cdd = Cdd0 + lambda*eye(size(Cdd0));

%% Build the model-data covariance matrix Cmd

% If they aren't already defined, create a set of lon/lat grid points to map to
if exist('xg','var')~=1
   [xg,yg] = meshgrid(-78:0.5:-61,31:0.5:42);
end

% Convert these to x,y in kilometers
ygkm = rearth*(yg(:)-ax(3))*pi/180/1000;
xgkm = rearth*(pi/180*(xg(:)-ax(1))) .* cos(pi/180*0.5*(yg(:)+ax(3))) /1000;

% distances between any pair of points
Xg = repmat(xgkm,[1 length(ykm)]);
Xd = repmat(xkm,[1 length(ygkm)]);
Yg = repmat(ygkm',[length(xkm) 1]);
Yd = repmat(ykm',[length(ygkm) 1]);
Rmd = sqrt((Xg-Xd').^2+(Yg'-Yd).^2);

%% Evaluate the normalized covariance using the fitted function
%  Use Markov: again with normalized covariance Cmd(0) and Cdd(0) = 1.
Cmd = (1+Rmd/b(2)).*exp(-Rmd/b(2));

%% Do the optimal interpolation ------------------------------------------

timer=cputime; 
D = mean(data) + Cmd*inv(Cdd)*(data-mean(data));
disp(['OI by inv(Cdd) took ' num2str(cputime-timer) ' seconds'])

timer=cputime; 
D = mean(data) + Cmd*(Cdd\(data-mean(data)));
disp(['OI by mldivide took ' num2str(cputime-timer) ' seconds'])
if pauseit; disp('paused...');pause; end

% Reshape to matrix so we can plot with pcolor
D = reshape(D,size(xg)); 

%% Map to original data locations so we can examine the residuals of the 
% optimal interpolation fit. This is done by simply using Cdd0 as the 
% Cmd matrix (i.e.the 'model' grid points are now just the data points). 
% Note that we don't use Cdd because Cdd has the error variance added to 
% the diagonal. We must use Cdd0, which was saved prior to adding the 
% error variance, for this to work.
D0 = mean(data) + Cdd0*inv(Cdd)*(data-mean(data));

figure(3)
hist(data-D0,20)
title('Histogram of residuals (data-OI)')
drawnow
if pauseit; disp('paused...');pause; end

figure(1) % so we can see it

figure(4)
clf
set(gcf,'pos',[3    34   909   303])
subplot(121)
pcolorjw(xg,yg,D)
caxis([2 23])
axis(ax)
pnc
title('Optimally interpolated solution')
if pauseit; disp('paused...');pause; end

hold on
han = scatter(xx,yy,30,data,'filled');
set(han,'markeredgecolor','k')
caxis(cax)
title('Optimally interpolated solution and data')
hold off
drawnow
if pauseit; disp('paused...');pause; end

%% Now compute expected error estimate
%
% E[e^2] = s^2 - Cmd inv(Cdd) Cmd'
% but we will plot this normalized by the signal variance s^2 so that the
% map shows the relative expected error. Where this = 1 the OI can provide
% no information about the solution that is better than the large scale
% mean (because the data are several covariance scales distant from the
% estimation point)
oierror = diag(1-Cmd*inv(Cdd)*Cmd');
oierror = reshape(oierror,size(xg));

figure(4)
subplot(122)
pcolorjw(xg,yg,oierror)
caxis([0 0.5])
colorbar
hold on
han = scatter(xx,yy,20,'k');
%set(han,'edgecolor','k','marker','o','markersize',2);
pnc
axis(ax)
hold off
drawnow
title('Normalized expected error')
if pauseit; disp('paused...');pause; end

% Calculate expected error at the data locations, multiplying by the signal
% variance this time to get dimensional values (deg C^2)
error0 = ssq*diag(1-Cdd0*inv(Cdd)*Cdd0');

figure(5)
set(gcf,'pos',[580   353   416   332])
plot(1:length(data),sqrt(error0),'r--',1:length(data),abs(data-D0),'.')
legend('expected error','actual |data-OI|')
within_limits = find(abs(data-D0)<=sqrt(error0));
xlabel('sample number')
ylabel('^oC')
titlestr = [int2str(round(100*length(within_limits)/length(data))) ...
  '% of residuals are within expected error bars'];
title(titlestr)
disp([titlestr ' (expect 68% for norm rand var)'])
