function Lab4()
%clear all % ������� ������
mx=512;
t=linspace(1,mx,mx);
r=4; % �������� ������������� �����������
a=-1;
b=0;
x(1)=-0.7; % ��������� �������
x(2)=r*x(1)*(1+x(1));
for k=1:mx
    x(k+1)=r*x(k)*(1+x(k));
    y(k*2)=x(k);
    y(k*2+1)=x(k);
end
p=linspace(a,b,2^10);
figure(1)% ���������� ��������� �������
%clf
plot(p,p) % �����������
hold on
plot(y(t),y(t+1),'red')
plot(p, r*p.*(1+p)) % ��������