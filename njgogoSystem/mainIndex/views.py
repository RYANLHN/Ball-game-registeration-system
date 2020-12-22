from django.shortcuts import render,reverse,redirect
from .form import *
from .models import *
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import UserCreationForm
import xlwt
from io import BytesIO
import math
import pandas as pd
from django.db.models import F,Q
import random
import re
import time
import datetime
from itertools import chain
# from django.contrib.auth.views import login

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect


def control(request,user):
   form = matchlistform()
   formb =exportform()
   formc=caipanlistform()
   controldic = {'user': request.user, 'form': form,'formb':formb,'formc':formc}
   if request.method=='GET':
      if str(request.user)==str(user):
         print(type(request.user))

         return render(request, 'loginIndex/control.html', controldic)
      else:
         logout(request)
         return HttpResponseRedirect(reverse('mainIndex:logined'))
         # return HttpResponse('aaaaa')
   else:
      c=request.user
      M=matchlist.objects.filter(createuser=c).values()
      # fenzu=fenzuform()
      if len(M)!=0:
         BMid=M[(len(M)-1)]['id']  #若很多人在不同的报名表报了名，可以不指定某一个报名表，直接用user

         player_list=playerlist.objects.filter(matchid=BMid).values()
         if playerlist.objects.filter(matchid=BMid,playerType='0').exists():  #团队报名
            # return HttpResponse(playerlist.objects.filter(matchid=BMid,playerType='0').values())
            #获得报名团队数量 "companylen"
            q=playerlist.objects.filter(matchid=BMid,playerType='0').values_list('playerCompany',flat=True)
            qdic={}
            for i in q:
               qdic[i]=qdic.get(i, 0) + 1
            companylen=len(qdic)
            #获得company文本供jq操作
            companyname=''
            for i in list(qdic.keys()):
               companyname+=(str(i)+',')
            companyname=companyname[:-1]
            player_num = '报名团队数量：' + str(companylen) + ' ' + '报名人数：' + str(len(player_list))
            #获取zb和cx，进行分组和制作赛程
            # playerround1=gainround1(companyname)


         else:   #独立报名
            player_num='全部报名人数：'+str(len(player_list))
            companyname=''
            #获取比赛种类matchtype
            typelist=matchlist.objects.filter(id=BMid).values('matchtype')[0]['matchtype'].split(',')
         a = {'user': c, 'player_list': player_list, 'num': len(player_list), 'player_numShow': player_num,'link': reverse('mainIndex:baoming', args=[c]), 'clist': companyname, 'typelist': typelist, 'BMid': BMid}

      else:
         player_list=['暂时未有报名者']
         a={'player_list':player_list}
      controldic.update(a)
      return render(request,"loginIndex/datacheck.html",controldic)   #嵌套页面

   # 'MS': MSplayer_list, 'MS_num': len(MSplayer_list),
   # 'FS': FSplayer_list, 'FS_num': len(FSplayer_list), 'MD': MDplayer_list, 'MD_num': len(MDplayer_list),
   # 'FD': FDplayer_list, 'FD_num': len(FDplayer_list), 'MIX': MSplayer_list, 'MIX_num': len(Mixplayer_list),

def logout_view(request):
   logout(request)
   return HttpResponseRedirect(reverse('mainIndex:logined'))

def logined(request):
   if request.method=='POST':
      form=userform(request.POST) #获取前端表单提交的内容
      if form.is_valid(): #验证表单中的内容是否合法
         username=form.cleaned_data['username']
         passwd=form.cleaned_data['passwd']
         aut=authenticate(username=username,password=passwd) #验证user
         if aut is not None:
            login(request,aut)  #传递username到request上
            # return HttpResponse('s')
            return HttpResponseRedirect(reverse('mainIndex:control',args=[username]))
         else:
            return HttpResponse('账号或密码错误，请联系工作人员')
      else:
         return HttpResponse('输入有误，请重新输入')

   else:
      # logout(request)
      webtitle='NJGOGO登陆页面'
      form= userform()
      mainIndexdic={'webtitle':webtitle,'form':form,'s':request.user}

      return render(request,'loginIndex/login.html',mainIndexdic)

def createuser(request):
   if request.method=='POST':
      form = UserCreationForm(data=request.POST)  # 获取前端表单内容
      if form.is_valid():  # 验证表单中的内容是否合法
         # username = form.cleaned_data['username']
         # passwd = form.cleaned_data['passwd']
         form.save()#把表单的数据存储到数据库

         return HttpResponse('创建成功')
      else:
         return HttpResponse('创建失败')
   else:
      form=UserCreationForm()
   return render(request,'loginIndex/createuser.html',{'form':form})

def generateBM(request,userN):
   BN=matchlist.objects.filter(createuser=userN).values()
   if len(BN)!=0:
      BNdic=BN[(len(BN)-1)]
      BNdic.update(forma=baominglistform())
      BNdic['matchtype']=BNdic['matchtype'].split(',')
      return render(request,'loginIndex/baoming.html',BNdic)
   else:
      return HttpResponse('用户还没有生成报名表')

def baoming(request,user):
   if request.method=='POST':
      matchinfo=matchlistform(request.POST)
      if matchinfo.is_valid():
         matchname=matchinfo.cleaned_data['matchname']
         matchtype=matchinfo.cleaned_data['matchtype']
         matchBMtype = matchinfo.cleaned_data['matchBMtype']
         matchlist.objects.create(matchname=matchname,createuser=user,matchtype=matchtype,matchBMtype=matchBMtype)
         # matchlistdic={'matchname':matchname,'matchtype':matchtype,'createuser':request.user}
         return generateBM(request,user)
      else:
         return HttpResponse('输入信息不合法')
   else:
      return generateBM(request, user)

def baomingsuccess(request,id):
   if request.method=='POST':
      playerinfo=baominglistform(request.POST)
      if playerinfo.is_valid():
         playerC=playerinfo.cleaned_data['company']
         contact = playerinfo.cleaned_data['contactPeople']
         contactN = playerinfo.cleaned_data['contactNumber']

         # gameT=playerinfo.cleaned_data['gametype']
         # player1N = playerinfo.cleaned_data['player1']
         # player1id = playerinfo.cleaned_data['player1id']
         # player2N = playerinfo.cleaned_data['player2']
         # player2id = playerinfo.cleaned_data['player2id']
         allplayer=playerinfo.cleaned_data['playerall']
         for i in allplayer.split(';'):
            a=i.split(',')
            if len(a)!=1:
               if a[1]!='':
                  player1N = a[1]
                  player1id = a[2]
                  player2N = a[3]
                  player2id = a[4]
                  gameT = a[5]
                  playerlist.objects.create(
                     matchid=id,
                     playerCompany=playerC,
                     playerType=gameT,
                     player1Name=player1N,
                     player1Id=player1id,
                     player2Name=player2N,
                     player2Id=player2id,
                     contact=contact,
                     contactNumber=contactN
                  )
         return HttpResponse('报名成功')
      else:
         return HttpResponse('输入有误')
   else:
      return HttpResponse('走错路了吧')

def createxhs(tt, id,gametype,hjg):
   if type(tt)==list:
      os = []
      if len(tt)%2==1:
         tt.append('轮空')
      for i in range(0, len(tt), 2):
         t = []
         t.append(tt[i])
         t.append(tt[i + 1])
         os.append(t)
      o = os
      for i in range(len(tt) - 1):
         hj = o[1][0]
         for u in range(1, len(o)):
            if u < (len(o) - 1):
               o[u][0] = o[u + 1][0]
            if u == (len(o) - 1):
               o[u][0] = o[u][1]
         for u in range(1, len(o)):
            o[len(o) - u][1] = o[len(o) - u - 1][1]
         o[0][1] = hj
         for g in range(len(o)):
            if o[g][0]!='轮空'and o[g][1]!='轮空':
               zhixuce.objects.create(matchid=id, gametype=gametype, zubie=hjg, lunshu=i + 1, changci=g + 1,player1=o[g][0], player2=o[g][1])


#赛程存入数据库函数
def savematch(request):
   exportinfo = exportform(request.POST)

   if exportinfo.is_valid():
      exp_gametype = exportinfo.cleaned_data['exp_gametype']
      exp_fenzuqk = exportinfo.cleaned_data['exp_fenzuqk'].split('：')[1:]
      exp_taotaiqk = exportinfo.cleaned_data['exp_taotaiqk'].split(',')
      M = matchlist.objects.filter(createuser=request.user).values()
      BMid = M[len(M) - 1]['id']

      all_fenzuqk = []
      if len(exp_fenzuqk) != playerlist.objects.filter(matchid=BMid, playerType=exp_gametype).count():
         for i in exp_fenzuqk:
            all_fenzuqk.append(i.split('|')[1:-1])
      else:
         for i in exp_fenzuqk:
            all_fenzuqk.append(i)
      #检查数据库是否有比赛项目数据，删除重建
      mk=fenzu.objects.filter(matchid=BMid,gametype=exp_gametype).count()
      if mk!=0:
         fenzu.objects.filter(matchid=BMid, gametype=exp_gametype).delete()
      ml = zhixuce.objects.filter(matchid=BMid, gametype=exp_gametype).count()
      if ml!=0:
         x = zhixuce.objects.filter(matchid=BMid, gametype=exp_gametype).values_list('id', flat=True)
         for m in x:
            saichang.objects.filter(zhixuceid=m).delete()
         zhixuce.objects.filter(matchid=BMid, gametype=exp_gametype).delete()

      for ig in range(len(all_fenzuqk)):
         fenzu.objects.create(matchid=BMid,gametype=exp_gametype,zubie=ig+1,fenzuqk=all_fenzuqk[ig])
         createxhs(all_fenzuqk[ig],BMid,exp_gametype,ig+1)
      for ug in range(0,len(exp_taotaiqk),2):
         # qq=str(exp_taotaiqk[ug])+'VS'+str(exp_taotaiqk[ug+1])
         zhixuce.objects.create(matchid=BMid, gametype=exp_gametype, zubie=0, lunshu=1, changci=int(ug/2+1),player1=exp_taotaiqk[ug],player2=exp_taotaiqk[ug+1])
      yy=int(math.log(len(exp_taotaiqk), 2))
      for hj in range(2,yy+1): #把淘汰赛后面的赛事都模拟生成
         for kk in range(int(math.pow(2,yy-hj))):
            # qq = str(2*kk+1) + 'VS' + str(2*kk+2)
            zhixuce.objects.create(matchid=BMid, gametype=exp_gametype, zubie=0, lunshu=hj, changci=kk+1,player1=str(2*kk+1),player2=str(2*kk+2))
      return HttpResponse('已保存分组')

   else:
      return HttpResponse('传入信息有误')

def export(request,user):
   exportdic={}
   if request.method == 'GET':
      return HttpResponse('不可以这样访问哦')
   else:
      M = matchlist.objects.filter(createuser=user).values()
      if len(M) != 0:
         BMid = M[(len(M) - 1)]['id']
         mname = M[(len(M) - 1)]['matchname']
      else:
         return HttpResponse('还没有报名表')

      # return HttpResponse(mname)

      # 设置HttpResponse的类型
      response = HttpResponse(content_type='application/vnd.ms-excel')
      response['Content-Disposition'] = 'attachment;filename='+mname+'.xls' #excel的改名！！！！！
      # cc = request.user


      baominglistinfo = playerlist.objects.filter(matchid=BMid).values_list()
      if len(baominglistinfo)==0:
         return HttpResponse('暂无报名信息')

      # 维护一些样式， style_heading, style_body, style_red, style_green

      style_heading = xlwt.easyxf("""
                      font:
                          name Arial,
                          colour_index white,
                          bold on,
                          height 0xA0;
                      align:
                          wrap off,
                          vert center,
                          horiz center;
                      pattern:
                          pattern solid,
                          fore-colour aqua;
                      borders:
                          left THIN,
                          right THIN,
                          top THIN,
                          bottom THIN;
                      """
                                  )

      style_body = xlwt.easyxf("""
                      font:
                          name Arial,
                          bold off,
                          height 0XA0;
                      align:
                          wrap on,
                          vert center,
                          horiz center;
                      borders:
                          left THIN,
                          right THIN,
                          top THIN,
                          bottom THIN;
                      """
                               )

      style_taotai = xlwt.easyxf("""
                            font:
                                name Arial,
                                bold off,
                                height 0XA0;
                            align:
                                wrap on,
                                vert center,
                                horiz left;
                            borders:
                                bottom MEDIUM;
                            """
                               )
      style_taotai2 = xlwt.easyxf("""
                                  font:
                                      name Arial,
                                      bold off,
                                      height 0XA0;
                                  align:
                                      wrap on,
                                      vert center,
                                      horiz left;
                                  borders:
                                      right MEDIUM,
                                      bottom MEDIUM;
                                  """
                                 )
      style_taotai3 = xlwt.easyxf("""
                                        font:
                                            name Arial,
                                            bold off,
                                            height 0XA0;
                                        align:
                                            wrap on,
                                            vert center,
                                            horiz left;
                                        borders:
                                            right MEDIUM;
   
                                        """
                                  )

      style_green = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x11;")
      style_red = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x0A;")
      fmts = [
         'M/D/YY',
         'D-MMM-YY',
         'D-MMM',
         'MMM-YY',
         'h:mm AM/PM',
         'h:mm:ss AM/PM',
         'h:mm',
         'h:mm:ss',
         'M/D/YY h:mm',
         'mm:ss',
         '[h]:mm:ss',
         'mm:ss.0',
      ]

      # new一个文件
      wb = xlwt.Workbook(encoding='utf-8')
      # new一个sheet
      sheet = wb.add_sheet(u'参赛者信息')

      # style_body.num_format_str = fmts[0]
      # 写标题栏
      sheet.write(0, 0, '参赛编号', style_heading)
      sheet.write(0, 1, '比赛编号', style_heading)
      sheet.write(0, 2, '队伍', style_heading)
      sheet.write(0, 3, '比赛项目', style_heading)
      sheet.write(0, 4, '运动员1', style_heading)
      sheet.write(0, 5, '身份证', style_heading)
      sheet.write(0, 6, '运动员2', style_heading)
      sheet.write(0, 7, '身份证', style_heading)
      sheet.write(0, 8, '联系人', style_heading)
      sheet.write(0, 9, '联系电话', style_heading)



      # 总报名信息
      for u in range(1,len(baominglistinfo)+1):
         sheet.write(u, 0, baominglistinfo[u-1][0], style_body)
         sheet.write(u, 1, baominglistinfo[u-1][1], style_body)
         sheet.write(u, 2, baominglistinfo[u-1][2], style_body)
         sheet.write(u, 3, baominglistinfo[u-1][3], style_body)
         sheet.write(u, 4, baominglistinfo[u-1][4], style_body)
         sheet.write(u, 5, baominglistinfo[u-1][5], style_body)
         sheet.write(u, 6, baominglistinfo[u-1][6], style_body)
         sheet.write(u, 7, baominglistinfo[u-1][7], style_body)
         sheet.write(u, 8, baominglistinfo[u-1][8], style_body)
         sheet.write(u, 9, baominglistinfo[u-1][9], style_body)

      type = matchlist.objects.filter(createuser=user).values_list('matchtype', flat=True)[len(M) - 1].split(',')

      sheet3=wb.add_sheet( u'秩序册') #制作秩序册sheet
      zhixucelist=zhixuce.objects.filter(Q(matchid=BMid) & ~Q(zubie=0)).exclude(Q(player1='轮空') | Q(player2='轮空')).order_by('lunshu','gametype','zubie','changci').values()
      taotailist=zhixuce.objects.filter(matchid=BMid,zubie=0).exclude(Q(player1='轮空') | Q(player2='轮空')).order_by('lunshu','gametype','changci').values()
      # return HttpResponse(zhixucelist)
      changdi=8 #场地数量
      changci=12 #能打多少个15分钟
      bisaidate= datetime.datetime.strptime('2020-12-15',"%Y-%m-%d")
      starttime=datetime.datetime.strptime('08:15',"%H:%M")
      sheet3.write(0,0,mname,style_heading)
      sheet3.write(1, 0, '场次', style_heading)
      sheet3.write(1, 1, '时间', style_heading)
      for i in range(changdi):
         sheet3.write(1, i+2,(str(i+1)+'号场地'), style_heading)
      roww=3
      # er=0
      for i in range(len(zhixucelist)):
         rr=math.floor(i/changdi)
         ee=math.floor(rr/changci)
         sheet3.write(roww+rr+ee, i%changdi+2, (zhixucelist[i]['gametype']+str(zhixucelist[i]['lunshu'])+str(zhixucelist[i]['zubie'])+str(zhixucelist[i]['changci'])), style_body)
         if i%changdi==0:
            sheet3.write(roww + rr+ee, 0, (rr%12)+1, style_body)
            sheet3.write(roww + rr+ee, 1, (starttime+(rr%changci)*(datetime.timedelta(minutes=15))+(ee%2)*(datetime.timedelta(minutes=330))).strftime("%H:%M"), style_body)
         # if rr%changci==0:

         #    sheet3.write(0, 1+ee, '赛时分割', style_body)
      for u in range(len(taotailist)):
         i=u+len(zhixucelist)
         rr = math.floor(i / changdi)
         ee = math.floor(rr / changci)
         sheet3.write(roww + rr + ee, i % changdi + 2, (taotailist[u]['gametype']+str(taotailist[u]['lunshu'])+str(taotailist[u]['zubie'])+str(taotailist[u]['changci'])), style_body)
         if i % changdi == 0:
            sheet3.write(roww + rr + ee, 0, rr, style_body)
            sheet3.write(roww + rr + ee, 1, (
                       starttime + (rr % changci) * (datetime.timedelta(minutes=15)) + (ee % 2) * (
                  datetime.timedelta(minutes=330))).strftime("%H:%M"), style_body)
         # if rr%changci==0:

      

      # 各个项目小组循环

      for t in type:
         row=0
         col=0
         bml = playerlist.objects.filter(matchid=BMid, playerType=t).values_list('playerCompany','player1Name','player2Name')
         if fenzu.objects.filter(matchid=BMid,gametype=t).exists(): #判断是否已经有生成分组
            uh=fenzu.objects.filter(matchid=BMid, gametype=t).values_list('zubie','fenzuqk')
            # return HttpResponse(len(uh))
            if len(uh)!=len(bml): #判断是否淘汰赛，若是小组赛，则生成循环sheet，若是淘汰赛则不生成
               sheet1 = wb.add_sheet(str(t) + u'小组循环')
               for q in range(len(uh)):
                  sheet1.write(q, 0, '第'+str(uh[q][0])+'组', style_heading)
                  au=uh[q][1][1:-1].split(',')
                  for w in range(len(au)):
                     if w==0:
                        sheet1.write(q, w+1, au[w][1:-1], style_body)
                     else:
                        sheet1.write(q, w + 1, au[w][2:-1], style_body)

               #计算胜场、胜次、胜分、名次
               #

               #编写小组积分表
               col=len(uh)+2+col
               row=len(uh)+2+row
               for q in range(len(uh)):
                  sheet1.write(row, 0, '第'+str(uh[q][0])+'组', style_heading)
                  row+=1
                  au = uh[q][1][1:-1].split(',')
                  #计算胜场、胜次、胜分、名次
                  saichangid=zhixuce.objects.filter(matchid=BMid,gametype=t,zubie=uh[q][0]).values_list('id',flat=True)
                  shengci={}
                  shengju={}
                  shengfen={}
                  for i in saichangid:
                     if saichang.objects.filter(zhixuceid=i).exists():
                        ui=saichang.objects.filter(zhixuceid=i).values()
                        apo=ui[len(ui)-1]['huosheng']
                        if apo in shengci.keys():
                           shengci[apo]+=1
                        else:
                           shengci[apo]=1
                        for f in ui:
                           bpo=f['huosheng']
                           cpo=f['huobai']
                           if bpo in shengju.keys():
                              shengju[bpo]+=1
                           else:
                              shengju[bpo] = 1
                           if bpo in shengfen.keys():
                              shengfen[bpo]+=abs(f['fenshu1']-f['fenshu2'])
                           else:
                              shengfen[bpo] = abs(f['fenshu1'] - f['fenshu2'])
                           if cpo in shengfen.keys():
                              shengfen[cpo]-=abs(f['fenshu1']-f['fenshu2'])
                           else:
                              shengfen[cpo] = -(abs(f['fenshu1'] - f['fenshu2']))
                  df=pd.DataFrame([shengci,shengju,shengfen],index=['shengci','shengju','shengfen'])
                  df2 = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
                  df3 = df2.sort_values(axis=0, ascending=False, by=['shengci','shengju','shengfen'])

                  chuxian=int((zhixuce.objects.filter(matchid=BMid,gametype=t,lunshu=1,zubie=0).count()*2)/len(uh))
                  # return HttpResponse(chuxian)
                  if df3.shape[0]!=0:
                     for j in range(chuxian):
                        if zhixuce.objects.filter(matchid=BMid, gametype=t, lunshu=1, zubie=0,player1=(str(uh[q][0])+str(j+1))).exists():
                           zhixuce.objects.filter(matchid=BMid, gametype=t, lunshu=1, zubie=0,player1=(str(uh[q][0])+str(j+1))).update(player1=df3.index.values[j])

                        else:
                           zhixuce.objects.filter(matchid=BMid, gametype=t, lunshu=1, zubie=0,player2=(str(uh[q][0]) + str(j + 1))).update(player2=df3.index.values[j])
                        # return HttpResponse(str(uh[q][0]) + str(j + 1))

                  for w in range(len(au)):
                     if w == 0:
                        sheet1.write(col, w+1, au[w][1:-1], style_body)
                        sheet1.write(row, 0, au[w][1:-1], style_body)
                        sheet1.write(row, len(au) + 1, au[w][1:-1], style_body)
                        if au[w][1:-1] in shengci.keys():
                           sheet1.write(row, len(au) + 2, shengci[au[w][1:-1]], style_body)
                        if au[w][1:-1] in shengju.keys():
                           sheet1.write(row, len(au) + 3, shengju[au[w][1:-1]], style_body)
                        if au[w][1:-1] in shengfen.keys():
                           sheet1.write(row, len(au) + 4, shengfen[au[w][1:-1]], style_body)
                           sheet1.write(row, len(au) + 5, df3.index.get_loc(au[w][1:-1])+1, style_body)
                        for s in range(w+1,len(au)):
                           if zhixuce.objects.filter(matchid=BMid,gametype=t,player1=au[w][1:-1],player2=au[s][2:-1]).exists():
                              zxc =zhixuce.objects.filter(matchid=BMid,gametype=t,player1=au[w][1:-1],player2=au[s][2:-1]).values()
                           else:
                              zxc = zhixuce.objects.filter(matchid=BMid, gametype=t, player1=au[s][2:-1],player2=au[w][1:-1]).values()

                           sheet1.write(row, s+1, str(zxc[0]['gametype'])+str(zxc[0]['lunshu'])+str(zxc[0]['zubie'])+str(zxc[0]['changci']), style_body)

                        row+=1
                     else:
                        sheet1.write(col, w + 1, au[w][2:-1], style_body)
                        sheet1.write(row, 0, au[w][2:-1], style_body)
                        sheet1.write(row, len(au) + 1, au[w][2:-1], style_body)
                        if au[w][2:-1] in shengci.keys():
                           sheet1.write(row, len(au) + 2, shengci[au[w][2:-1]], style_body)
                        if au[w][2:-1] in shengju.keys():
                           sheet1.write(row, len(au) + 3, shengju[au[w][2:-1]], style_body)
                        if au[w][2:-1] in shengfen.keys():
                           sheet1.write(row, len(au) + 4, shengfen[au[w][2:-1]], style_body)
                           sheet1.write(row, len(au) + 5, df3.index.get_loc(au[w][2:-1])+1, style_body)
                        for s in range(w+1,len(au)):
                           if zhixuce.objects.filter(matchid=BMid,gametype=t,player1=au[w][2:-1],player2=au[s][2:-1]).exists():
                              zxc =zhixuce.objects.filter(matchid=BMid,gametype=t,player1=au[w][2:-1],player2=au[s][2:-1]).values()
                           else:
                              zxc = zhixuce.objects.filter(matchid=BMid, gametype=t, player1=au[s][2:-1],player2=au[w][2:-1]).values()
                           if len(zxc)!=0:
                              sheet1.write(row, s+1, str(zxc[0]['gametype'])+str(zxc[0]['lunshu'])+str(zxc[0]['zubie'])+str(zxc[0]['changci']), style_body)
                        for y in range(w):
                           if y==0:
                              if zhixuce.objects.filter(matchid=BMid,gametype=t,player1=au[w][2:-1],player2=au[y][1:-1]).exists():
                                 zxc =zhixuce.objects.filter(matchid=BMid,gametype=t,player1=au[w][2:-1],player2=au[y][1:-1]).values()
                              else:
                                 zxc = zhixuce.objects.filter(matchid=BMid, gametype=t, player1=au[y][1:-1],player2=au[w][2:-1]).values()
                              if len(zxc)!=0:
                                 ee1=saichang.objects.filter(zhixuceid=zxc[0]['id'],huosheng=au[w][2:-1]).count()
                                 ee2=saichang.objects.filter(zhixuceid=zxc[0]['id'], huosheng=au[y][1:-1]).count()
                                 # return HttpResponse(zxc)
                                 if ee1!=0 or ee2!=0:
                                    sheet1.write(row, y+1, (str(ee1)+':'+str(ee2)), style_body)

                           else:
                              if zhixuce.objects.filter(matchid=BMid,gametype=t,player1=au[w][2:-1],player2=au[y][2:-1]).exists():
                                 zxc =zhixuce.objects.filter(matchid=BMid,gametype=t,player1=au[w][2:-1],player2=au[y][2:-1]).values()
                              else:
                                 zxc = zhixuce.objects.filter(matchid=BMid, gametype=t, player1=au[y][2:-1],player2=au[w][2:-1]).values()
                              if len(zxc)!=0:
                                 ee1=saichang.objects.filter(zhixuceid=zxc[0]['id'],huosheng=au[w][2:-1]).count()
                                 ee2=saichang.objects.filter(zhixuceid=zxc[0]['id'], huosheng=au[y][2:-1]).count()
                                 # return HttpResponse(zxc)
                                 if ee1!=0 or ee2!=0:
                                    sheet1.write(row, y+1, (str(ee1)+':'+str(ee2)), style_body)

                        row += 1
                  sheet1.write(col, len(au) + 1, '运动员', style_body)
                  sheet1.write(col, len(au) + 2, '胜次', style_body)
                  sheet1.write(col, len(au) + 3, '胜局', style_body)
                  sheet1.write(col, len(au) + 4, '胜分', style_body)
                  sheet1.write(col, len(au) + 5, '名次', style_body)
                  row = row+1
                  col = row
                  # col = 0

            #创建淘汰赛的sheet
            taotai=zhixuce.objects.filter(matchid=BMid, gametype=t,zubie=0,lunshu=1).values_list('player1','player2')
            taotai1l=[]
            for i in taotai:
               taotai1l.append(i[0])
               taotai1l.append(i[1])
            # return HttpResponse(len(taotai1l))
            sheet2=wb.add_sheet(str(t)+u'淘汰赛')
            taotail=len(taotai1l)
            k=int(math.log(taotail,2))
            for u in range(k+1):
               for i in range(int(taotail/math.pow(2,u))):
                  if u==0:
                     sheet2.write(int(math.pow(2,u)*(2*i+1)), 2*u, taotai1l[i], style_taotai)
                     if i%2==1:

                        sheet2.write(int(math.pow(2, u) * (2 * i + 1)), 2 * u + 1, '', style_taotai2)
                     else:
                        for y in range((int(math.pow(2,u)*(2*i+1))+1),int(math.pow(2,u)*(2*i+3))):
                           sheet2.write(y, 2 * u+1, '', style_taotai3)
                        sheet2.write(int(math.pow(2, u) * (2 * i + 1)), 2 * u + 1, '', style_taotai)

                  elif u==k:
                     sheet2.write(int(math.pow(2, u) * (2 * i + 1)), 2 * u, '', style_taotai)
                     sheet2.write(int(math.pow(2, u) * (2 * i + 1)), 2 * u + 1, '', style_taotai)

                  else:
                     sheet2.write(int(math.pow(2, u) * (2 * i + 1)), 2*u, '', style_taotai)
                     if i%2==1:

                        sheet2.write(int(math.pow(2, u) * (2 * i + 1)), 2 * u + 1, '', style_taotai2)
                     else:
                        for y in range((int(math.pow(2,u)*(2*i+1))+1),int(math.pow(2,u)*(2*i+3))):
                           sheet2.write(y, 2 * u+1, '', style_taotai3)
                        sheet2.write(int(math.pow(2, u) * (2 * i + 1)), 2 * u + 1, '', style_taotai)


         # else:
         #    return HttpResponse(str(t)+'还没有')




      # 写出到IO
      output = BytesIO()
      wb.save(output)
      # 重新定位到开始
      output.seek(0)
      response.write(output.getvalue())
      return response



      # gain={'exp_gametype':exp_gametype,'exp_fenzuqk':all_fenzuqk,'exp_taotaiqk':exp_taotaiqk,'baominglistinfo':baominglistinfo,'user':request.user}
      # exportdic.update(gain)
      # return render(request,'loginIndex/export.html',exportdic)

   #1、淘汰赛选择后不显示小组sheet，淘汰sheet显示姓名，除种子选手外随机排位 done
   #2、小组赛淘汰环节排序 11 82 12 72 13 62.。 done
   #3、取消淘汰排序选项，淘汰按照随机排序，小组按照交叉排序s done
def lufen(request,BMid):
   form=lufenform()
   formc = jifentrigger()
   lufendic={'form':form,'formc':formc}
   if request.method=='GET':
      return HttpResponse('不允许这样访问')
   else:
      zhixucelist = zhixuce.objects.filter(Q(matchid=BMid) & ~Q(zubie=0)).exclude(Q(player1='轮空') | Q(player2='轮空')).order_by('lunshu', 'gametype', 'zubie','changci')
      taotailist = zhixuce.objects.filter(matchid=BMid, zubie=0).exclude(Q(player1='轮空') | Q(player2='轮空')).order_by('lunshu', 'gametype', 'changci')

      changdi = 8  # 场地数量
      changci = 12  # 能打多少个15分钟
      bisaidate = datetime.datetime.strptime('2020-12-15', "%Y-%m-%d")
      starttime = datetime.datetime.strptime('08:15', "%H:%M")

      a=[]
      for i in range(changdi):
         a.append(str(i + 1) + '号场地')
      lufendic.update({'title':a,'width':(98.25/(changdi+2)),'widthbody':((98.25/(changdi+2))*changdi),'widthbodyl':98/(changdi),'zhixucelist':zhixucelist,'taotailist':taotailist,'BMid':BMid})

      # # roww = 3
      # for i in range(len(zhixucelist)):
      #    rr = math.floor(i / changdi)
      #    ee = math.floor(rr / changci)
      #    if i % changdi == 0:
      #       sheet3.write(roww + rr + ee, 0, rr, style_body)
      #       sheet3.write(roww + rr + ee, 1, (starttime + (rr % changci) * (datetime.timedelta(minutes=15)) ).strftime("%H:%M"), style_body)
      b=[]
      d=[]
      for i in range(int(math.ceil((len(zhixucelist)+len(taotailist))/changdi))):
         bd=int(math.floor(i/12))
         b.append((starttime + int(i%12) * (datetime.timedelta(minutes=15))+(bd%2)* (datetime.timedelta(minutes=330)) ).strftime("%H:%M"))
         d.append((i%12)+1)
      lufendic.update({'time':b,'bianhao':d})
      q=saichang.objects.values_list('zhixuceid',flat=True)
      qdic = {}
      for i in q:
         qdic[i] = qdic.get(i, 0) + 1
      havelufen=''
      for u in list(qdic.keys()):
         havelufen+=(str(u)+',')
      havelufen=havelufen[:-1]
      lufendic.update({'qdic':havelufen})

      return render(request, 'loginIndex/lufen.html', lufendic)

def uploadbifen(request):
   if request.method=='GET':
      return HttpResponse('不能这样访问哦')
   else:
      lfform=lufenform(request.POST)
      if lfform.is_valid():
         zhixuceID=lfform.cleaned_data['zhixuceID']
         if saichang.objects.filter(zhixuceid=zhixuceID).exists():
            saichang.objects.filter(zhixuceid=zhixuceID).delete()
         shengli1 = lfform.cleaned_data['shengli1']
         shibai1 = lfform.cleaned_data['shibai1']
         bifen11 = lfform.cleaned_data['fenshu11']
         bifen12 = lfform.cleaned_data['fenshu12']
         saichang.objects.create(zhixuceid=zhixuceID,huosheng=shengli1,huobai=shibai1,fenshu1=bifen11,fenshu2=bifen12)
         shengli2 = lfform.cleaned_data['shengli2']
         shibai2 = lfform.cleaned_data['shibai2']
         bifen21 = lfform.cleaned_data['fenshu21']
         bifen22 = lfform.cleaned_data['fenshu22']
         saichang.objects.create(zhixuceid=zhixuceID, huosheng=shengli2, huobai=shibai2, fenshu1=bifen21,fenshu2=bifen22)
         shengli3 = lfform.cleaned_data['shengli3']
         if shengli3!='-1':
            shibai3 = lfform.cleaned_data['shibai3']
            bifen31 = lfform.cleaned_data['fenshu31']
            bifen32 = lfform.cleaned_data['fenshu32']
            saichang.objects.create(zhixuceid=zhixuceID, huosheng=shengli3, huobai=shibai3, fenshu1=bifen31,fenshu2=bifen32)
         return HttpResponse(zhixuceID+'分数录入成功')
      else:
         return HttpResponse('输入信息不合法')

def printjifenbiao(request,BMid):
   if request.method=='GET':
      return HttpResponse('不可以这样访问')
   else:
      zhixuceinfo=jifentrigger(request.POST)
      if zhixuceinfo.is_valid():
         zhixuceid=zhixuceinfo.cleaned_data['zhixuceid']
         localT = time.localtime()
         info=zhixuce.objects.filter(id=zhixuceid).values()
         name=str(info[0]['gametype'])+str(info[0]['lunshu'])+str(info[0]['zubie'])+str(info[0]['changci'])
         matchname=matchlist.objects.filter(id=info[0]['matchid']).values('matchname')[0]['matchname']
         startdate = time.strftime('%Y-%m-%d', localT)
         starttime = time.strftime('%H:%M', localT)
         player1=info[0]['player1']
         player2 = info[0]['player2']
         if re.match('(.*)-',player1,re.I):
            if re.match('-(.*?)\+',player1,re.I):
               p11=re.findall(r'-(.*?)\+',player1,re.I)[0]
               p12=re.findall(r'\+(.*)',player1,re.I)[0]
               d1=re.findall(r'(.*)-',player1,re.I)[0]
               p21 = re.findall(r'\+(.*)', player2, re.I)[0]
               p22 = re.findall(r'\+(.*)', player2, re.I)[0]
               d2= re.findall(r'(.*)-', player2, re.I)[0]
            else:
               p11=re.findall(r'-(.*)',player1,re.I)[0]
               p12=''
               d1 = re.findall(r'(.*)-', player1, re.I)[0]
               p21 = re.findall(r'-(.*)', player2, re.I)[0]
               p22=''
               d2 = re.findall(r'(.*)-', player2, re.I)[0]
         else:
            p11=player1
            p12=''
            p21=player2
            p22=''
            d1=''
            d2=''
         nn=[]
         for i in range(52):
            nn.append(' ')
         caipan=caipanall.objects.filter(matchid=BMid).values_list('caipan',flat=True)
         jifenbiaodic={'name':name,'matchname':matchname,'player1':player1,'player2':player2,'startdate':startdate,'starttime':starttime,'nn':nn,'namesize':(70/len(name)),'d1size':(192/len(player1)),'player2size':(192/len(player2)),'p11':p11,'p12':p12,'p21':p21,'p22':p22,'caipan':caipan,'d1':d1,'d2':d2}
         return render(request,'loginIndex/jifenbiao.html', jifenbiaodic)
      else:
         return HttpResponse('输入信息不合法')

def savecaipan(request):
   if request.method == 'POST':
      M = matchlist.objects.filter(createuser=request.user).values()
      if len(M) != 0:
         BMid = M[(len(M) - 1)]['id']
      caipaninfo=caipanlistform(request.POST)
      if caipaninfo.is_valid():
         caipan=caipaninfo.cleaned_data['caipanlist']
         if caipanall.objects.filter(matchid=BMid).exists():
            caipanall.objects.filter(matchid=BMid).delete()
         ca=caipan.split('、')
         for i in ca:
            caipanall.objects.create(matchid=BMid,caipan=i)

         return HttpResponse('成功添加教练')
      else:
         return HttpResponse('输入不合法')
   else:
      return HttpResponse('不能这样访问')
