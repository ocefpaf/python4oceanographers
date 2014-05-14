function misfit = myfunction(a,x,fx,method)
% misfit = myfunction(a,x,fx,method)
% Compute the mean squared misfit between an analytical function
% (e.g. Gaussian or Markov function) and a set of data FX observed at
% independent coordinates X.
%
% a = parameters of analytical function
% x = locations of data
% fx = observed function values (data)
% method (optional) specifies the shape of the function to be fitted:
%        Must be one of = 'Gaussian', 'Markov' (default) or 'LeTraon'
%
% For use in conjunction with fminsearch
%
% In all cases, two parameters are fit
% a(1) is the y-intercept at x=0
% a(2) is the characteristic scale of the fitted function

if nargin < 4
  method = 'Markov';
end

switch lower(method(1:5))
  case 'gauss'
    % Gaussian function
    % f = a0*exp(-0.5*(r/a)^2)
    r = x/a(2);
    fit = a(1)*exp(-0.5*r.^2);
    
  case 'marko'
    % Markov function
    % f = a0*(1+r/a)*exp(-r/a)
    r = abs(x)/a(2);
    fit = a(1)*(1+r).*exp(-r);
    
  case 'letra'
    % Le Traon function
    % f = a0*exp(-r/a)*(1+r/a+(r^2)/6-(r^3)/6
    r = abs(x)/a(2);
    rsq = r.^2;
    fit = a(1)*exp(-r).*(1+r+rsq/6-(r.*rsq)/6);
end

misfit = mean((fit-fx).^2);