##### dbinfo page ######
@login_required
def info(request):
    template_name = 'application/info.html'
    principal = False
    company_list = []
    if request.user.is_authenticated:
        user_id=request.user.id
        superuser=request.user.is_superuser
        if superuser == 0:
            company_id = company_user.objects.get(user_id=user_id).company_admin_id
            company_admin_ob = company_admin.objects.get(id=company_id)
            cid = company_admin_ob.company_id
            try:
                if company_admin_ob.principal_id == user_id:
                    principal = True
            except Exception as e:
                print(e)
        else:
            company_ip = ''
            company_list = company_admin.objects.all()

            if request.POST.get('company', '')!='':
                request.session['company']=request.POST.get('company', '')
            try:
                cid=int(request.session['company'])
            except Exception as e:
                print(e)
                request.session['company']=company_list[0].company_id
                cid=int(request.session['company'])


    if request.GET.get('date1', '')!='':
        request.session['date1'] = request.GET.get('date1', '')
    else:
        request.session['date1'] = str(datetime.date.today()-datetime.timedelta(days=3))#-datetime.timedelta(days=7))
    if request.GET.get('date2', '')!='':
        request.session['date2'] = request.GET.get('date2', '')
    else:
        request.session['date2'] = str(datetime.date.today())


    try:
        date1 = request.session['date1']
        date2 = request.session['date2']


        with MyMongo() as conn:
            dbinfo = conn.query_in('dbinfo', int(cid))
            cpucount = conn.query_in('cpucount', int(cid))
            memory = conn.query_in('Tibero_Shared_Memory', int(cid))



    except Exception as e:
        print(e)
    try:
        update_time = dbinfo[0]['datetime']
    except Exception as e:
        print(e)
        dbinfo = ()
        cpucount = ()
        update_time = datetime.datetime.now()

    return render(request, template_name,
                  {'cid':cid, 'update_time':update_time, 'date1':date1, 'date2':date2, 'dbinfo':dbinfo,
                  'principal':principal, 'cpucount':cpucount, 'superuser':superuser, 'company_list':company_list,
                  'memory': memory
                  })




@login_required
def tbspace(request):
    template_name = 'application/tbspace.html'
    principal = False
    if request.user.is_authenticated:
        user_id=request.user.id
        superuser=request.user.is_superuser
        if superuser == 0:
            company_id = company_user.objects.get(user_id=user_id).company_admin_id
            company_admin_ob = company_admin.objects.get(id=company_id)
            company_ip = company_admin_ob.company_ip
            cid = company_admin_ob.company_id
            try:
                if company_admin_ob.principal_id == user_id:
                    principal = True
            except Exception as e:
                print(e)
        else:
            company_ip = ''
            company_list = company_admin.objects.all()
            if request.POST.get('company', '')!='':
                request.session['company']=request.POST.get('company', '')
            try:
                cid=int(request.session['company'])

            except:
                request.session['company']=company_list[0].company_id
                cid=int(request.session['company'])


    date1_f = datetime.datetime.strptime(request.session['date1'], '%Y-%m-%d')
    date2_f = datetime.datetime.strptime(request.session['date2'], '%Y-%m-%d')+datetime.timedelta(days=1)
    tbname = 'tbspace'
    try:
        with MyMongo() as conn:
            find = conn.query_in(tbname, int(cid), date1_f, date2_f)

        df = pd.DataFrame(i for i in find).drop('timestamp', axis=1, errors='ignore')
        table = list(df['Tablespace'].unique())

        tbspace = {}
        tbspace_f = {}
        for i in table:
            tbspace[i] = df.loc[df['Tablespace']== i].drop('Tablespace', axis=1).values.tolist()
            tbspace_f[i] = df.loc[df['Tablespace']== i].drop('Tablespace', axis=1).values.tolist()[::6]
        update_time = tbspace['SYSTEM'][-1][1]
    except Exception as e:
        print(e)
        tbspace = {}
        tbspace_f = {}
        update_time = datetime.datetime.now()
        table=[]


    return render(request, template_name, {'tbspace':tbspace, 'tbspace_f':tbspace_f, 'table':table, 'update_time':update_time})
