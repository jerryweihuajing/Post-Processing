from pylab import *

fig = figure(figsize=(10,8))
sigma3 = 5.0

d = np.genfromtxt('sigma3='+str(sigma3)+'MPa.txt')

plot(d[:,0],d[:,1])
max_stress = max(d[:,1])
#print(type (max_stress))
pos = d[:,0][list(d[:,1]).index(max_stress)] #find out the maximum point
print (max_stress)
scatter([pos,],[max_stress],20,color='blue')
plot([pos,pos],[0,max_stress],color='blue',linestyle='--')
plot([-0.2,pos],[max_stress,max_stress],color='blue',linestyle='--')
annotate('Max Stress =  %.2f MPa' % max_stress,
         xy = (pos, max_stress),
         xycoords = 'data',
         xytext = (-100,+10),
         textcoords = 'offset points',
         fontsize = 15)
annotate(r'$\sigma_3$ = '+str(sigma3)+'MPa',
         xy = (1.5, 0),
         xycoords = 'data',
         xytext = (+10, +30),
         textcoords = 'offset points',
         fontsize=20)
xlabel(r'$\varepsilon_1$ [%]', fontsize = 20)
ylabel(r'$\sigma_1-\sigma_3$ [MPa]', fontsize=20)
xlim([-0.2,20]),ylim([0,max_stress*1.05])
xticks(fontsize=12), yticks(fontsize=12)
show()

fig.savefig('sigma3='+str(sigma3)+'MPa.png')