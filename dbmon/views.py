from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import HttpResponseRedirect, Http404, render
from django.contrib.auth.decorators import login_required


from django.template.defaulttags import register

from accounts.models import company_admin, company_user
import datetime, time

from db import MyMongo
from pexcept import PrintException

# Views

class HomePage(TemplateView):
    template_name = 'index.html'

    def get(self, request, **kwargs):
        principal = False
        try:
            if request.session['temp'] == '1':
                self.temp = request.session['temp']
            else:
                request.session['temp'] = request.GET.get('temp', '')
        except Exception as e:
            request.session['temp'] = request.GET.get('temp', '')

        if request.user.is_authenticated:
            user_id = request.user.id
            self.superuser = request.user.is_superuser
            if self.superuser == 0:
                company_id = company_user.objects.get(user_id=user_id).company_admin_id
                company_admin_ob = company_admin.objects.get(id=company_id)
                company_ip = company_admin_ob.company_ip
                self.cid = company_admin_ob.company_id
                try:
                    if company_admin_ob.principal_id == user_id:
                        principal = True
                except Exception as e:
                    print(e)
            else:
                company_ip = ''
                self.company_list = company_admin.objects.all()
                if request.POST.get('company', '') != '':
                    request.session['company'] = request.POST.get('company', '')
                try:
                    self.cid= request.session['company']

                except:
                    request.session['company'] = company_list[0].company_id
                    self.cid = request.session['company']

            self.temp = request.session['temp']
            self.dbname = 'cid_'+str(self.cid)

            if request.GET.get('date', '') != '': request.session['date'] = request.GET.get('date', '')
            else:
                if 'date' in request.session: pass
                else: request.session['date'] = str(datetime.date.today())

            self.date = request.session['date']

            try:
                with MyMongo(database=self.dbname) as conn:
                    self.host_list = conn.query_one('dbmon_Dbinfo', 'host_name')

                if request.GET.get('host', '') != '': request.session['host'] = request.GET.get('host', '')
                else:
                    if 'host' in request.session: pass
                    else: request.session['host'] = self.host_list[0]

                self.host = request.session['host']
            except Exception as e:
                PrintException()

            try:

                yesterday = datetime.datetime.strptime(self.date, '%Y-%m-%d')-datetime.timedelta(days=1)
                yesterday = yesterday.strftime('%Y-%m-%d')
                start_d = datetime.datetime.combine(datetime.datetime.strptime(self.date, '%Y-%m-%d'), datetime.time.min)
                end_d = datetime.datetime.combine(datetime.datetime.strptime(self.date, '%Y-%m-%d'), datetime.time.max)
                with MyMongo(database=self.dbname) as conn:
                    daliy_desc = conn.query_in('dbmon_DailyDesc', request.session['host'], start_d,end_d)
                    report_time = conn.query_in('dbmon_DailyReport', request.session['host'], start_d,end_d)
                    disk = conn.query_in('dbmon_DiskUsage', request.session['host'], start_d-datetime.timedelta(days=1),end_d-datetime.timedelta(days=1))
                print(disk)

                interval_list = [i['starttime'].strftime("%Y-%m-%d %H:%M:%S")+" ~ "+ i['endtime'].strftime("%Y-%m-%d %H:%M:%S") for i in report_time]

                if request.GET.get('interval', '')!='': request.session['interval'] = request.GET.get('interval', '')
                else:
                    if 'interval' in request.session :
                        if not request.session['interval']: request.session['interval'] = interval_list[0]
                        else: pass
                    else:
                        try: request.session['interval'] = interval_list[0]
                        except: request.session['interval'] = None

                interval = request.session['interval']

                time = interval.split('~')
                start, end = datetime.datetime.strptime(time[0].strip(), "%Y-%m-%d %H:%M:%S"), datetime.datetime.strptime(time[1].strip(), "%Y-%m-%d %H:%M:%S")
                with MyMongo(database=self.dbname) as conn:
                    perf_sum = conn.query_in('dbmon_PerfRecord', self.host, start, end)
                    info = conn.query('dbmon_DailyReport', {'host_name':self.host, 'starttime':start, 'endtime':end})


                info[0]['reason'] = info[0]['reason'].upper().replace('_', ' ')
            except Exception as e:
                PrintException()

        else:
            return HttpResponseRedirect(reverse('login'))


        return render(request, self.template_name, locals())

    def post(self, request, **kwargs):
        return self.get(request, **kwargs)
