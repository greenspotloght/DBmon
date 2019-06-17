from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required


from accounts.models import company_admin, company_user

import pandas as pd
import datetime, time
import math

from db import MyMongo
from pexcept import PrintException

######## parent class ##########
class DashBoard_View(LoginRequiredMixin, TemplateView):
    template_name = ''

    def get(self, request, **kwargs):
        self.principal = False
        company_list = []
        if request.user.is_authenticated:
            user_id=request.user.id
            self.superuser=request.user.is_superuser
            if self.superuser == 0:
                company_id = company_user.objects.get(user_id=user_id).company_admin_id
                company_admin_ob = company_admin.objects.get(id=company_id)
                self.cid = company_admin_ob.company_id
                try:
                    if company_admin_ob.principal_id == user_id:
                        self.principal = True
                except Exception as e:
                    print(e)
            else:
                company_ip = ''
                self.company_list = company_admin.objects.all()

                if request.POST.get('company', '')!='':
                    request.session['company']=request.POST.get('company', '')
                try:
                    self.cid=request.session['company']
                except Exception as e:
                    print(e)
                    request.session['company']=self.company_list[0].company_id
                    self.cid=request.session['company']


        if request.GET.get('date1', '')!='':
            request.session['date1'] = request.GET.get('date1', '')
        else:
            request.session['date1'] = str(datetime.date.today()-datetime.timedelta(days=3))#-datetime.timedelta(days=7))
        if request.GET.get('date2', '')!='':
            request.session['date2'] = request.GET.get('date2', '')
        else:
            request.session['date2'] = str(datetime.date.today())

        self.temp = request.session['temp']
        self.date1 = request.session['date1']
        self.date2 = request.session['date2']
        self.dbname = 'cid_'+str(self.cid)



        try:
            with MyMongo(database=self.dbname) as conn:
                self.host_list = conn.query_one('dbmon_Dbinfo', 'host_name')

            if request.GET.get('host', '')!='': request.session['host'] = request.GET.get('host', '')
            else: request.session['host'] = self.host_list[0]
            self.host = request.session['host']

        except:
            PrintException()

    def post(self, request, **kwargs):
        return self.get(request, **kwargs)


class Chart_View(LoginRequiredMixin, TemplateView):
    template_name = ''

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            user_id=request.user.id
            superuser=request.user.is_superuser
            if superuser == 0:
                company_id = company_user.objects.get(user_id=user_id).company_admin_id
                company_admin_ob = company_admin.objects.get(id=company_id)
                company_ip = company_admin_ob.company_ip
                self.cid = company_admin_ob.company_id
                try:
                    if company_admin_ob.principal_id == user_id:
                        self.principal = True
                except Exception as e:
                    print(e)
            else:
                company_ip = ''
                company_list = company_admin.objects.all()
                if request.POST.get('company', '')!='':
                    request.session['company']=request.POST.get('company', '')
                try:
                    self.cid=request.session['company']

                except:
                    request.session['company']=company_list[0].company_id
                    self.cid=request.session['company']

            self.temp = request.session['temp']
            self.date1_f = datetime.datetime.strptime(request.session['date1'], '%Y-%m-%d')
            self.date2_f = datetime.datetime.strptime(request.session['date2'], '%Y-%m-%d')+datetime.timedelta(days=1)
            self.dbname = 'cid_'+str(self.cid)

######test info ########





# Create your views here.
################### dbinfo page #########################
################### dbinfo page ########################
class DBInfo(DashBoard_View):
    template_name = 'application/dbinfo/info.html'

    def get(self, request, **kwargs):
        super(DBInfo, self).get(request, **kwargs)
        principal = self.principal
        try:
            with MyMongo(database=self.dbname) as conn:
                dbinfo = conn.query_in('dbmon_Dbinfo', request.session['host'])
                cpucount = conn.query_in('dbmon_Cpucount', request.session['host'])
                memory = conn.query_in('dbmon_Tsm', request.session['host'])

        except Exception as e:
            PrintException()
            print(e)
        try:
            update_time = dbinfo[0]['datetime']
        except Exception as e:
            PrintException()
            print(e)
            dbinfo = ()
            cpucount = ()
            update_time = datetime.datetime.now()

        return render(request, self.template_name, locals())


######## tbspace chart #########
class tbspace_chart(Chart_View):
    template_name = 'application/dbinfo/tbspace.html'

    def get(self, request, **kwargs):
        super(tbspace_chart, self).get(request, **kwargs)
        tbname = 'dbmon_Tbspace'
        try:
            with MyMongo(database=self.dbname) as conn:
                find = conn.query_in(tbname, request.session['host'], self.date1_f, self.date2_f)

            df = pd.DataFrame(i for i in find).drop('timestamp', axis=1, errors='ignore')
            table = list(df['Tablespace'].unique())

            tbspace = {}
            tbspace_f = {}
            for i in table:
                tbspace[i] = df.loc[df['Tablespace']== i].drop('Tablespace', axis=1).values.tolist()
                tbspace_f[i] = df.loc[df['Tablespace']== i].drop('Tablespace', axis=1).values.tolist()[::6]


            update_time = tbspace['SYSTEM'][-1][0]
        except Exception as e:
            PrintException()
            print(e)
            update_time = datetime.datetime.now()

        return render(request, self.template_name, locals())

######## sga_pga chart #########
class sga_chart(Chart_View):
    template_name = 'application/dbinfo/sga.html'

    def get(self, request, **kwargs):
        super(sga_chart, self).get(request, **kwargs)
        tbname = 'dbmon_Sga'
        try:
            with MyMongo(database=self.dbname) as conn:
                sga = conn.query_in(tbname, request.session['host'], self.date1_f, self.date2_f)

            sga_df = pd.DataFrame(i for i in sga).drop('timestamp', axis=1, errors='ignore')
            sga_dict = sga_df.to_dict('record')
            update_time = sga_dict[-1]['datetime']


        except Exception as e:
            PrintException()
            print(e)
            sga_dict = []

        return render(request, self.template_name, locals())


######## pga chart #########
class pga_chart(Chart_View):
    template_name = 'application/dbinfo/pga.html'

    def get(self, request, **kwargs):
        super(pga_chart, self).get(request, **kwargs)
        tbname = 'dbmon_Pga'
        try:
            with MyMongo(database=self.dbname) as conn:
                pga = conn.query_in(tbname, request.session['host'], self.date1_f, self.date2_f)

            pga_df = pd.DataFrame(i for i in pga).drop('timestamp', axis=1, errors='ignore')
            pga_dict = pga_df.to_dict('record')
            update_time = pga_dict[-1]['datetime']

        except Exception as e:
            PrintException()
            print(e)
            pga_dict = []

        return render(request, self.template_name, locals())


######## sga_pga chart #########
class dbsize_chart(Chart_View):
    template_name = 'application/dbinfo/dbsize.html'

    def get(self, request, **kwargs):
        super(dbsize_chart,self).get(request, **kwargs)
        tbname = 'dbmon_Dbsize'
        try:
            with MyMongo(database=self.dbname) as conn:
                find = conn.query_in(tbname, request.session['host'], self.date1_f, self.date2_f)

            df = pd.DataFrame(i for i in find).drop('timestamp', axis=1, errors='ignore')

            dbsize = df.to_dict('record')
            dbsize = dbsize[::6]
            update_time = dbsize[-1]['datetime']

        except Exception as e:
            PrintException()
            print(e)
            dbsize = []

        return render(request, self.template_name, locals())


######## session chart #########
class session_chart(Chart_View):
    template_name = 'application/dbinfo/session.html'
    def get(self, request, **kwargs):
        super(session_chart, self).get(request, **kwargs)
        tbname = 'dbmon_Session'

        with MyMongo(database=self.dbname) as conn:
            find = conn.query_in(tbname, request.session['host'], self.date1_f, self.date2_f)

        df = pd.DataFrame(i for i in find).drop('timestamp', axis=1, errors='ignore')
        session = df.to_dict('record')


        return render(request, self.template_name, locals())

################### dbinfo page end  #########################





#################### ratio page ###############################
#################### ratio_hit page ##########################
class Ratio(DashBoard_View):
    template_name = 'application/ratio/ratio_page.html'

    def get(self, request, **kwargs):
        super(Ratio, self).get(request, **kwargs)
        principal = self.principal
        try:
            date1_f = datetime.datetime.strptime(request.session['date1'], '%Y-%m-%d')
            date2_f = datetime.datetime.strptime(request.session['date2'], '%Y-%m-%d')+datetime.timedelta(days=1)

            try:
                with MyMongo(database=self.dbname) as conn:
                    dict_ratio = conn.query_in('dbmon_DictionaryCacheHitRatio', request.session['host'], date1_f, date2_f)
                    sql_ratio = conn.query_in('dbmon_SQLCacheHitRatio', request.session['host'], date1_f, date2_f)
                    buffer_ratio = conn.query_in('dbmon_BufferCacheHitRatio', request.session['host'], date1_f, date2_f)

                dict_ratio = pd.DataFrame(i for i in dict_ratio).drop('timestamp', axis=1, errors='ignore')
                sql_ratio = pd.DataFrame(i for i in sql_ratio).drop('timestamp', axis=1, errors='ignore')
                buffer_ratio = pd.DataFrame(i for i in buffer_ratio).drop('timestamp', axis=1, errors='ignore')

                dict_ratio = dict_ratio.to_dict('record')
                sql_ratio = sql_ratio.to_dict('record')
                buffer_ratio = buffer_ratio.to_dict('record')


            except Exception as e:
                PrintException()
                print(e)

        except Exception as e:
            PrintException()
            print(e)

        try:
            update_time = dbinfo[0]['datetime']
        except Exception as e:
            PrintException()
            print(e)
            dbinfo = ()
            cpucount = ()
            update_time = datetime.datetime.now()

        return render(request, self.template_name, locals())


#################### perf page ##########################
class Perf(DashBoard_View):
    template_name = 'application/perf/perf_page.html'

    def get(self, request, **kwargs):
        super(Perf, self).get(request, **kwargs)
        principal = self.principal

        if request.GET.get('time1', '')!='': request.session['time1'] = request.GET.get('time1', '')
        else: request.session['time1'] = str(datetime.time.min)

        if request.GET.get('time2', '')!='': request.session['time2'] = request.GET.get('time2', '')
        else: request.session['time2'] = str(datetime.time(1,0,0,0))

        if request.GET.get('date', '')!='': request.session['date'] = request.GET.get('date', '')
        else: request.session['date'] = str(datetime.date.today()-datetime.timedelta(days=1))

        self.time1 = request.session['time1']
        self.time2 = request.session['time2']
        self.date = request.session['date']
        time1 = datetime.datetime.strptime(self.date+' '+self.time1, '%Y-%m-%d %H:%M:%S')
        time2 = datetime.datetime.strptime(self.date+' '+self.time2, '%Y-%m-%d %H:%M:%S')


        try:
            with MyMongo(database=self.dbname) as conn:
                perf = conn.query_in('dbmon_PerfRecord', request.session['host'], time1, time2)

            perf = pd.DataFrame(i for i in perf)
            perf = perf.to_dict('record')
            # if perf
        except Exception as e:
            PrintException()
            print(e)



        try:
            update_time = dbinfo[0]['datetime']
        except Exception as e:
            PrintException()
            print(e)
            dbinfo = ()
            cpucount = ()
            update_time = datetime.datetime.now()

        return render(request, self.template_name, locals())
