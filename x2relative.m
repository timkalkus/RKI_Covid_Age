function [ x_rel ] = x2relative( x )
%X2RELATIVE Summary of this function goes here
%   Detailed explanation goes here
pos=get(gca,'Position');
x_rel = interp1(xlim,[pos(1) pos(1)+pos(3)], x,'linear', 'extrap');

end

