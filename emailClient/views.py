
# coding:utf8   这句话 不是一句简单的注释 ，加了后 ，本文件中的汉子 就可以识别了


from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout


from smtplib import SMTP, SMTP_SSL
from smtplib import SMTPRecipientsRefused
from poplib import POP3
from time import sleep
import sys
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import poplib
import email
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from django.contrib import admin
from  models import myEmail

#from django.contrib.admin import logout

import  sys, os
# Create your views here.
smtpserver = 'smtp.qq.com'
pop3server = 'pop.qq.com'
emailaddr = '75039960@qq.com'
username = '75039960'
#password = 'dvnmpwfyvlsocbda'
password = 'dvnmpwfyvlsocbda'
password = 'yyqsxoajfqstbhgd'

adminUser='lgl'
adminPwd ='hello888'
adminEmail = '75039960@qq.com'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@login_required
def login(request):
    return HttpResponseRedirect('/home/')

@login_required
def  home( request):
    test = 1
    test += 2
    return render(request, "style.html", locals(),context_instance=RequestContext(request))
    #return HttpResponse("hello")

def  inbox( request):
    #RecvEmail()


    emailList = myEmail.objects.all()

    return render_to_response('inbox.html', {'courseList': emailList},context_instance=RequestContext(request))
    #return render(request, "inbox.html", locals())


def  outbox( request):
    #RecvEmail()


    return render_to_response('outbox.html')

def  logout( request):
    admin.logout(request)
    return HttpResponse("logout")

def  contact(request):
    return HttpResponseRedirect('/admin/emailClient/')
    #return render(request, "contact.html", locals())

def  callsend(request):
    errs =''
    sendSer = SMTP_SSL(smtpserver)
    sendSer.set_debuglevel(1)
    print sendSer.ehlo()[0]  # 服务器属性等
    sendSer.login(username, password)  # qq邮箱需要验证

    try:
        #if(request.method== 'post'):

        content = 'smtplib test: hello, smtplib ! Can you see it ?'

        if( request.POST.has_key('Content')):
            content = request.POST['Content']

        textApart = MIMEText(content)

        #imageFile = BASE_DIR + '/static/image/cat.jpg'

        #imageApart = MIMEImage(file(imageFile, 'rb').read(), imageFile.split('.')[-1])
        #imageApart.add_header('Content-Disposition', 'attachment', filename=imageFile.split('/')[-1])


        subject = request.POST['Subject']
        m = MIMEMultipart()
        m.attach(textApart)
        #m.attach(imageApart)
        fromaddr = emailaddr
        toaddrs = emailaddr
        if (request.POST.has_key('SendTo')):
            toaddrs = request.POST['SendTo']

        m['Subject'] = subject
        m['From'] = fromaddr
        m['To'] = toaddrs


        # errs = sendSer.sendmail(emailaddr, emailaddr, origMsg)
        errs = sendSer.sendmail(fromaddr, toaddrs, m.as_string())
    except SMTPRecipientsRefused:
        print 'server refused....'
        sendSer.quit()
        #return HttpResponse( 'server refused....')
        render_to_response('send.html', {'bFlag': 1})
        #sys.exit(1)
    sendSer.quit()
    #assert len(errs) == 0, errs
    print errs

    print '\n\n\nsend a mail ....OK!\n\n'
    #render_to_response('send.html')
    #return HttpResponse("send  already ") #HttpResponseRedirect('/')
    #return  HttpResponseRedirect('/home')
    #return render(request, "send.html", locals())
    #return render(request, "send.html", {'bFlag': 0})
    #render_to_response('send.html', {'bFlag': 0})
    #emailList = myEmail.objects.all()[0:3]
    #return render_to_response('inbox.html', {'emailList': emailList, 'len': 0})


    return render(request, "sendAfter.html", locals(),context_instance=RequestContext(request))


def  send(request):
    #sleep(3)  # 等待10秒
    #print 'Now get the mail .....\n\n\n'
    return render(request, "send.html", locals(),context_instance=RequestContext(request))


# 开始接收邮件
#revcSer = POP3(pop3server)
def  RecvEmail( ):
    revcSer = poplib.POP3_SSL(pop3server)
    revcSer.user(username)
    revcSer.pass_(password)
    print revcSer.list()
    numMessages = len(revcSer.list()[1])
    print 'num of emails in box = ', numMessages

    rsp, msg, siz = revcSer.retr(revcSer.stat()[0])
    sep = msg.index('')
    print  'rsp =', rsp,  'size = ',siz
    if msg:
        for i in msg:
            print i
    revcBody = msg[sep + 1:]

    print  'Body= ',revcBody[5]
    #assert origBody == revcBody
    #print 'successful get ....'
    #return


    #emailList = myEmail.objects.all()
    #return render_to_response('inbox.html', {'courseList': emailList})


def  fecthall(request):
    revcSer = poplib.POP3_SSL(pop3server)
    revcSer.user(username)
    revcSer.pass_(password)
    numMessages = len(revcSer.list()[1])
    print ' object count  ==', myEmail.objects.all().count()

    # 从最老的邮件开始遍历

    myEmail.objects.all().delete()
    numMessages = len(revcSer.list()[1])
    print 'all num of messages 2222 = ', numMessages


    for i in range(numMessages):
        msgBody =''
        m = revcSer.retr(i + 1)
        print 'id = ',  i

        msg = email.message_from_string('\n'.join(m[1]))


        #print 'msg=', msg
        # allHeaders = email.Header.decode_header(msg)
        aimHeaderStrs = {'from': '', 'to': '', 'subject': ''}
        for aimKey in aimHeaderStrs.keys():
            aimHeaderList = email.Header.decode_header(msg[aimKey])
            for tmpTuple in aimHeaderList:
                if tmpTuple[1] == None:
                    aimHeaderStrs[aimKey] += tmpTuple[0]
                else:
                    aimHeaderStrs[aimKey] += tmpTuple[0].decode(tmpTuple[1])  # 转成unicode


        for aimKey in aimHeaderStrs.keys():
            print aimKey, ':', aimHeaderStrs[aimKey].encode('utf-8')  # 转成utf-8显示

        for part in msg.walk():  # 遍历所有payload
            contenttype = part.get_content_type()
            filename = part.get_filename()
            if filename:  # and contenttype=='application/octet-stream':
                # 保存附件
                #data = part.get_payload(decode=True)
                #file("mail%d.attach.%s" % (i + 1, filename), 'wb').write(data)
                print 'filename =',filename
            elif contenttype == 'text/plain':
                # 保存正文
                data = part.get_payload(decode=True)
                #charset = part.get_content_charset('ios-8859-1')
                charset = part.get_content_charset('utf-8')# ('gb2312')
                #file('mail%d.txt' % (i + 1), 'w').write(data.decode(charset).encode('utf-8'))
                print 'msgbody=' ,data.decode(charset).encode('utf-8')
                msgBody = data.decode(charset).encode('utf-8')

        mye = myEmail.objects.create(From=aimHeaderStrs['from'],
                                         To=aimHeaderStrs['to'],
                                         Subject=aimHeaderStrs['subject'],
                                          Content = msgBody,
                                          Type = 0,
                                     )
        mye.save()
    emailList = myEmail.objects.all()
    for   e in emailList:
        #print 'from:',e.From ,'to:',e.To, 'sub:', e.Subject, 'content:',e.Content
        print 'from:', e.From.decode('utf-8').encode('utf-8'), 'to:', \
            e.To.decode('utf-8').encode('utf-8'), 'sub:', e.Subject.decode('utf-8').encode('utf-8'),\
            'content:', e.Content.encode('utf-8')
    #print 'emailList===',emailList
    print 'len===', len(emailList)
    return render_to_response('inbox.html', {'emailList': emailList,  'len': len(emailList)},context_instance=RequestContext(request))
