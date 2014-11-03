% echo off
% more on
pauseit = 0;

% fraction of data to retain for mapping
frac = 0.05;

% random error to add to obs (in obs units, here deg C)
e = 0.75;

%% regular grid of coordinates to map data to
[xg,yg] = meshgrid(-78:(1/3):-61,31:(1/3):42);

if exist('temp','var')~=1
  load ../data/mercator_temperature.mat
end
[xx,yy] = meshgrid(x,y);
k = 10; % depth index into Mercator data
data = squeeze(temp(k,:,:));

% plot these data
cax = [2 23];
figure(1)
set(gcf,'pos',[4   386   909   303])
clf
subplot(121)
pcolorjw(x,y,data)
caxis(cax)
title(['Temperature at ' int2str(depth(k)) ...
  ' m from Mercator analysis 2004-Mar-01'])
% draw coastline
try
  pnc
catch
end
if pauseit; disp('paused...');pause; end

bad = find(isnan(data)==1);
xx(bad) = [];
yy(bad) = [];
data(bad) = [];

%% Decimate the data
% Generate N random numbers between 1 and N - we will retain only these
% elements of the data
N = length(data(:));
rm = round(N*rand([1 round(frac*N)]));
% can't have index < 1 or > N
rm = min(N,max(1,rm));

disp(['retaining ' int2str(100*length(rm)/length(data(:))) '% of data']);
xx = xx(rm);
yy = yy(rm);
data = data(rm);

figure(1)
subplot(122)
han = scatter(xx,yy,20,data,'filled');
caxis(cax)
try
  pnc
catch
end
axis(ax)
title('Subsampled ''data'' locations')
drawnow
if pauseit; disp('paused...');pause; end

%% Assuming isotropic and homogeneous variability, make an estimate of the
%  data covariance function by computed binned-lagged covariance for all
%  possible data-data pairs

% Get distances separating every pair of stations using approximate
% spherical calculation
xx = xx(:);
yy = yy(:);
data = data(:);
rearth = 6370800; % metres

% xkm, ykm will be the coordinates of the data (converted from lon/lat)
ykm = rearth*(yy-ax(3))*pi/180/1000;
xkm = rearth*(pi/180*(xx-ax(1))) .* cos(pi/180*0.5*(yy+ax(3))) /1000;

% Build matrices that repeat columns of x and rows of y. Then X-X' and Y-Y'
% will be all possible distance combinations between pairs of points
X = repmat(xkm,[1 length(ykm)]);
Y = repmat(ykm',[length(xkm) 1]);
Rdd = sqrt((X-X').^2+(Y-Y').^2);

% triu sets the lower triangle to zeros. we don't want those points because
% they are duplicates of the upper triangle (xi-xj) = -(xj-xi)
Rddu = triu(Rdd);

%% Add some random noise to data
disp(['Adding random noise of +/- ' num2str(e) ' deg C'])
disp(['               or variance ' num2str(e^2) ' deg C^2'])
data = data + e*randn(size(data));
if pauseit; disp('paused...');pause; end

%% Compute the binnned lagged covariance function

% remove mean before calculating covariance
d = data-mean(data);

% covariance
C = d*d';

% set the distance bins
dr = 30;
r = [0 0.5*dr:dr:1000];

% variance of samples that fall into each bin
clear cf
cf(1) = mean(diag(C));
for i=2:length(r)
  tmp = find(Rddu(:)>r(i)-0.5*dr & Rddu(:)<=r(i)+0.5*dr);
  cf(i) = mean(C(tmp));
end

figure(2)
set(gcf,'pos',[12   382   469   302])
han = plot(r,cf,'x');grid on
xlabel('distance (km)')
ylabel('^oC^2')
title('Binned lagged covariance from data')
if pauseit; disp('paused...');pause; end

% Now fit an analytical covariance function to the data.
% In this example I limit the fit to values in r < 600 km. Don't fit to
% the zero lag data because it has the error variance included, and don't
% go out to very long lags because the covariance there is based on very
% few estimates)
rfitmax = 600;
subset = find(r>0 & r<=rfitmax);

% help fminsearch does not fully document that you can pass additional
% 4th, 5th ... etc arguments that are passed through to myfunction
% [20 400] are starting guesses for the optimal fits
a = fminsearch('myfunction',[20 400],[],r(subset),cf(subset),'gauss');
b = fminsearch('myfunction',[20 400],[],r(subset),cf(subset),'markov');

% final fit at convergence
misfit_a = myfunction(a,r(subset),cf(subset),'gauss');
misfit_b = myfunction(b,r(subset),cf(subset),'marko');

% c = fminsearch('myfunction',[20 400],[],r(subset),cf(subset),'letra');
% misfit_c = myfunction(c,r(subset),cf(subset),'letra');

% estimate the noise variance
if misfit_a < misfit_b
  best_method = 'Gaussian';
  esq = cf(1)-a(1);
  han_to_change = 2;
else
  best_method = 'Markov';
  esq = cf(1)-b(1);
  han_to_change = 3;
end
disp(['The best fit was for function form: ' best_method])

% plot the binned covariance estimate and the function fits
han = plot(r,cf,'x',...
  r,a(1)*exp(-0.5*(r/a(2)).^2),...
  r,b(1)*(1+r/(b(2))).*exp(-r/b(2)));

% make the line thicker for the best fit
set(han(han_to_change),'linewidth',2)
grid on
labels = { 'data',...
  ['Gaussian: misfit = ' num2str(misfit_a)],...
  ['Markov:   misfit = ' num2str(misfit_b)]};
legend(labels)
if pauseit; disp('paused...');pause; end

hold on
plot([150 150],[cf(1)-esq cf(1)],'k-',150,cf(1)-esq,'kv',150,cf(1),'k^')
text(160,b(1)+0.7*esq,'e^2')
hold off
ylim([-5 20])
labels{4} = ['error std dev = ' num2str(sqrt(esq))];
legend(labels)
xlabel('distance (km)')
ylabel('^oC^2')
drawnow

disp(['Random noise variance added was       ' num2str(e^2)])
disp(['   Error variance estimated was ' num2str(esq)])
