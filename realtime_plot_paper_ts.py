

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Cursor
from matplotlib.font_manager import FontProperties
from matplotlib.widgets import CheckButtons

import time

fig = plt.figure(figsize=(10, 7))
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)
buf = 1000
show_frames=1
show_anchors=1
show_dummies=0
show_ts=1
font_per = [{'family': 'serif',
        'color':  'k',
        'size': 12,
        },{'family': 'serif',
        'color':  'k',
        # 'weight': 'bold',
        'size': 24,
        }]

ax_rtxen = plt.axes([0, 0.91, 0.2, 0.12])
ax_rtxen.text(0.06,0.42,'Average VM1 CPU utilization(%/sec):',fontdict=font_per[0])
ax_rtxen_txt = ax_rtxen.text(0.1,0.01,'%.2f%%'%(0),fontdict=font_per[1])
ax_rtxen.axis('off')


ax_xen = plt.axes([0.65, 0.91, 0.2, 0.12])
ax_xen.text(0.08,0.42,'Average VM2 CPU utilization(%/sec):',fontdict=font_per[0])
ax_xen_txt = ax_xen.text(0.4,0.01,'%.2f%%'%(0),fontdict=font_per[1])
ax_xen.axis('off')

last_ts=[15,15]

def animate2(i):
    maxx=30000

    global last_ts,show_frames, show_anchors, show_dummies, ax_xen_txt,ax_rtxen_txt,show_ts

    pullData = open("info.txt","r").read()
    minmax = open("minmax.txt","r").read()
    dataArray = pullData.split('\n')
    minmaxArray = minmax.split('\n')
    time_start=0
    time_end=0

    x = []
    hrs = []
    cpus_xs  =[]
    cpus = []
    anchor_xs = []
    anchors = []
    frame_xs = []
    frames = []
    dummy_x = []
    dummy_hrs = []
    ts_xs = []
    ts = []
    event_last_happened_at_cnt=[-1,-1]

    for i in range(2):
        x.append([])
        hrs.append([])  
        cpus_xs.append([])    
        cpus.append([])
        anchor_xs.append([])
        anchors.append([])
        frame_xs.append([])
        frames.append([])
        dummy_x.append([])
        dummy_hrs.append([])        
        ts_xs.append([])
        ts.append([])




        # for j in range(buf):
        #     x[i].append(j)
        #     hrs[i].append(0)
        #     cpus[i].append(0)
    cnt=0
    maxhrs=0
    for eachLine in dataArray:
        if len(eachLine)>1:
            line = eachLine.split()
            if cnt==0:
                time_start = float(line[-1])
            time_end = float(line[-1])
            index=int(line[0])-23
            if len(line)==3+1:
                x[index].append(float(line[-1])-time_start)
                hrs[index].append(float(line[1]))

            if len(line)==2+1:
                # print(line)
                anchor_xs[index].append(float(line[-1])-time_start)
                anchors[index].append(int(line[1]))
                event_last_happened_at_cnt[index]=cnt

            if len(line)==4+1:
                frame_xs[index].append(float(line[-1])-time_start)
                frames[index].append(int(line[1]))
                event_last_happened_at_cnt[index]=cnt

            if len(line)==5+1:
                dummy_x[index-2].append(float(line[-1])-time_start)
                dummy_hrs[index-2].append(float(line[1]))
            if len(line)==6+1:
                ts_xs[index].append(float(line[-1])-time_start)
                ts[index].append(int(line[1]))
                last_ts[index]=int(line[1])
                event_last_happened_at_cnt[index]=cnt
            if len(line)==7+1:
                cpus_xs[index].append(float(line[-1])-time_start)
                cpus[index].append(float(line[1])*100)


            cnt+=1
    min_max = []
    for eachLine in minmaxArray:
        if len(eachLine)>1:
            line = eachLine.split()
            min_max.append(float(line[1]))

    ax1.clear()
    ax2.clear()
    sched=["VM1","VM2"]
    colrs = ['blue','limegreen']
    for i in range(len(x)):
        ax1.scatter(x[i],hrs[i],s= ((1)%2)*6+5 ,label= sched[i] ,color=colrs[i])
        ax2.plot(cpus_xs[i],cpus[i],color=colrs[i],lw=((i+1)%2)+3,label= sched[i] )
        # tmp=[]
        # for j in range(len(cpus[i])):
        #     tmp.append(100-cpus[i][j])
        # ax2.plot(x[i],tmp,color=dummy_colrs[i],lw=((i+1)%2)+3,label= sched[i] )
        # ax2.scatter(x[i],cpus[i],s= ((i+1)%2)*6+5,label= sched[i] ,color=colrs[i])
    dummy_colrs = ['cyan','lightgreen']
    dummy_sched=["Dummy\nRT-Xen","Dummy\nCredit"]

    if show_dummies:
        for i in range(len(dummy_x)):
            ax1.scatter(dummy_x[i],dummy_hrs[i],s= ((1)%2)*6+5 ,label= dummy_sched[i] ,color=dummy_colrs[i],marker='o')

    x_for_minmax = []
    miny = []
    maxy = []
    total_x_len = len(x[0])+len(x[1])+len(dummy_x[0])+len(dummy_x[1])
    for i in range(total_x_len):
        x_for_minmax.append(i)
        miny.append(min_max[0])
        maxy.append(min_max[1])
    if time_start>0 and time_end>0 and len(miny)>1:
        ax1.plot([0,time_end-time_start],miny[0:2],'r')
        # ax1.plot([0,time_end-time_start],[(miny[0]+maxy[0])/2,(miny[0]+maxy[0])/2],'pink')
        ax1.plot([0,time_end-time_start],[(miny[0]+maxy[0])/2,(miny[0]+maxy[0])/2],'pink')
        ax1.plot([0,time_end-time_start],maxy[0:2],'r',label= 'Target\nFPS\nInterval')
    fontP = FontProperties()
    fontP.set_size('small')
    ax1.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.,prop=fontP)
    # ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.12),ncol=3, fancybox=True, shadow=True,prop=fontP)
    # ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),ncol=3, fancybox=True, shadow=True,prop=fontP)
    ax2.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.,prop=fontP)
    # fig.suptitle('RT-Xen vs Credit', fontsize=14, fontweight='bold')
    per = 0
    # try:
    #     rtxen_fps = hrs[0][-1]
    #     credit_fps = hrs[1][-1]
    #     per=(rtxen_fps-credit_fps)/credit_fps*100
   

    try:
        hrs_after_event_rtxen=0
        hrs_after_event_rtxen_cnt=0
        hrs_after_event_credit=0
        hrs_after_event_credit_cnt=0
        for ii,xx in enumerate(hrs[0]):
            if x[0][ii]>event_last_happened_at_cnt[0]:
                hrs_after_event_rtxen+=xx
                hrs_after_event_rtxen_cnt+=1
        for ii,xx in enumerate(hrs[1]):
            if x[1][ii]>event_last_happened_at_cnt[1]:
                hrs_after_event_credit+=xx
                hrs_after_event_credit_cnt+=1
        if hrs_after_event_rtxen_cnt > 0 and hrs_after_event_rtxen_cnt >0:
            rtxen_fps = hrs_after_event_rtxen/hrs_after_event_rtxen_cnt
            credit_fps = hrs_after_event_credit/hrs_after_event_credit_cnt
            per=(rtxen_fps-credit_fps)/credit_fps*100
    except:
        per=0

    area_under_curve_rtxen=0
    area_under_curve_xen=0
    if len(cpus_xs[1])>0:
        for i in range(1,len(cpus_xs[1])):
            area_under_curve_xen+=cpus[1][i-1]*(cpus_xs[1][i]-cpus_xs[1][i-1])
    if len(cpus_xs[0])>0:
        for i in range(1,len(cpus_xs[0])):
            area_under_curve_rtxen+=cpus[0][i-1]*(cpus_xs[0][i]-cpus_xs[0][i-1])


    if area_under_curve_xen>0:
        ax_xen_txt.set_text('%.2f%%'%(area_under_curve_xen/(cpus_xs[1][-1]-cpus_xs[1][0])))
    if area_under_curve_rtxen>0:
        ax_rtxen_txt.set_text('%.2f%%'%(area_under_curve_rtxen/(cpus_xs[0][-1]-cpus_xs[0][0])))

    # ax1.set_title('RT-Xen improved by: %.2f %%'%(per)+"\n",loc='right',fontdict=font_per[1])
    # ax1.set_title(r'$\frac{RT-Xen\'s improvement}{Percentage}$ = %.2f %%'%(per)+"\n",loc='right',fontsize=18)
    # ax1.set_title(r'$\frac{RT-Xen \quad FPS}{Credit \quad FPS }$ = %.2f %%'%(per)+"\n",loc='right',fontsize=18)
    # ax1.set_xlabel('Time\n \n')
    ax2.set_xlabel('Time')
    ax1.set_ylabel('Moving Average FPS(frames/sec) \n (Window Size = 12)')
    ax2.set_ylabel('Assigned CPU Time (%)')
    # ax2.set_ylim( 45, 105 )  
    ax2.set_ylim( -5, 105 )  
    # ax1.set_xlim(0,200)
    # ax2.set_xlim(0,200)
    ax=[ax1, ax2]
    font = [{'family': 'serif',
            'color':  'dodgerblue',
            'weight': 'bold',
            'size': 8,
            },{'family': 'serif',
            'color':  'forestgreen',
            'weight': 'bold',
            'size': 8,
            }]
    colrs = ['dodgerblue','forestgreen']

    if show_anchors:
        for i in range(len(anchor_xs)):
            for j in range(len(anchor_xs[i])):
                ax1.axvline(x=anchor_xs[i][j],color=colrs[i], linestyle='-')
                ax2.axvline(x=anchor_xs[i][j],color=colrs[i], linestyle='-')
                ymin,ymax=ax1.get_ylim()
                if anchors[i][j]==0:
                    ax1.text(anchor_xs[i][j],ymax,"50%",rotation=45,fontdict=font[i])
                elif anchors[i][j]==2:
                    ax1.text(anchor_xs[i][j],ymax,"100%",rotation=45,fontdict=font[i])
                elif anchors[i][j]==1:
                    ax1.text(anchor_xs[i][j],ymax,"Linear",rotation=45,fontdict=font[i])
                elif anchors[i][j]==3:
                    ax1.text(anchor_xs[i][j],ymax,"APID",rotation=45,fontdict=font[i])
                elif anchors[i][j]==4:
                    ax1.text(anchor_xs[i][j],ymax,"AIMD",rotation=45,fontdict=font[i])
    if show_frames:
        for i in range(len(frame_xs)):
            for j in range(len(frame_xs[i])):
                ax1.axvline(x=frame_xs[i][j],color=colrs[i], linestyle='--')
                ax2.axvline(x=frame_xs[i][j],color=colrs[i], linestyle='--')
                ax2.text(frame_xs[i][j],-10,"period: "+str(frames[i][j]),rotation=45,fontdict=font[i],horizontalalignment='right',verticalalignment='top')
    if show_ts:
        for i in range(len(ts_xs)):
            for j in range(len(ts_xs[i])):
                ax1.axvline(x=ts_xs[i][j],color=colrs[i], linestyle=':')
                ax2.axvline(x=ts_xs[i][j],color=colrs[i], linestyle=':')
                ax2.text(ts_xs[i][j],10,"ts: "+str(ts[i][j]),rotation=45,fontdict=font[i],horizontalalignment='right',verticalalignment='top')




ani = animation.FuncAnimation(fig, animate2, interval=1000)


# rax = plt.axes([0.91, 0.01, 0.085, 0.2])
# rax.axis('off')
# check = CheckButtons(rax, ['Show\nFrames','Show\nAnchors','Show\nTimeslice' ], [True,True,True])

# # check_per = CheckButtons(rax_per, ['Show\nFrames'], [True])

# def func(label):
#     global show_frames, show_anchors,show_dummies,show_ts
#     if 'Anchors' in label:
#       show_anchors=(show_anchors+1)%2
#     elif 'Frames' in label:
#       show_frames=(show_frames+1)%2    
#     elif 'Dummies' in label:
#       show_dummies=(show_dummies+1)%2
#     elif 'Timeslice' in label:
#       show_ts=(show_ts+1)%2

#     return
# check.on_clicked(func)
# # cursor = Cursor(rax, useblit=True, color='m', linewidth=2)


plt.show()


# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import time

# fig = plt.figure()
# ax1 = fig.add_subplot(2,1,1)
# ax2 = fig.add_subplot(2,1,2)
# buf = 1000
# def animate(i):
#     pullData = open("info.txt","r").read()
#     dataArray = pullData.split('\n')
#     x = []
#     hrs = []
#     cpus = []
#     cnt=[]
#     for i in range(2):
#         x.append([])
#         hrs.append([])
#         cpus.append([])
#         cnt.append(-1)
#         for j in range(buf):
#             x[i].append(j)
#             hrs[i].append(0)
#             cpus[i].append(0)
#     for eachLine in dataArray:
#         if len(eachLine)>1:
#             line = eachLine.split()
#             index=int(line[0])-1
#             cnt[index]+=1
#             hrs[index][cnt[index]]=(float(line[1]))
#             cpus[index][cnt[index]]=(float(line[2])/10000)
#     for i in range(2):
#         hrs[i]=hrs[i][:buf]
#         cpus[i]=cpus[i][:buf]

#     ax1.clear()
#     ax2.clear()
#     opts=['r*','bo']
#     for i in range(len(x)):
#         ax1.plot(x[i],hrs[i],opts[i],markersize=((i+1)%2)*2+1)
#         ax2.plot(x[i],cpus[i],opts[i],markersize=((i+1)%2)*3+1)

# ani = animation.FuncAnimation(fig, animate, interval=1000)
# plt.show()


