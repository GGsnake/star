from django.conf.urls import url
from adc import views, net, query, login, sql

urlpatterns = [

    url(r'^login', login.loginindex, name='log'),
    url(r'^enlogin', login.login, name='enlogin'),
    url(r'^upFirbe', net.upFirbe, name='upFirbe'),
    url(r'^upChannel', net.upChannel, name='upChannel'),
    url(r'^upWsr', net.upWsr, name='upWsr'),
    url(r'^upCab', net.upCab, name='upCab'),
    url(r'^index', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^setting', views.setting, name='setting'),


    url(r'^get', login.login, name='login'),
    url(r'^out', login.loginout, name='out'),

    url(r'^Fibe', views.FibeView, name='Fibe'),
    url(r'^Cable', views.Cabview, name='Cabview'),
    url(r'^Channel', views.ChannelView, name='Channel'),
    url(r'^Wsr', views.Wsr, name='Wsr'),
    url(r'^Uses', views.Uses, name='Uses'),

    url(r'^Show', views.Show, name='Show'),
    url(r'^ChShow', views.ChShow, name='Show'),
    url(r'^CaShow', views.CabShow, name='CaShow'),
    url(r'^WsShow', views.WsrShow, name='WsShow'),


    url(r'^add', views.add, name='add'),
    url(r'^Chadd', views.chadd, name='Chadd'),
    url(r'^Cabadd', views.cabadd, name='Cabadd'),


    url(r'^deletfirbe', sql.deletfirbe, name='deletfirbe'),
    url(r'^chdeletfirbe', sql.chdeletfirbe, name='chdeletfirbe'),
    url(r'^cabdeletfirbe', sql.cabdeletfirbe, name='cabdeletfirbe'),
    url(r'^Wetfirbe', sql.Wetfirbe, name='Wetfirbe'),
    url(r'^deluser', sql.deluser, name='deluser'),


    url(r'^update', sql.update, name='update'),
    url(r'^chupdate', sql.chupdate, name='chupdate'),
    url(r'^cabupdate', sql.cabupdate, name='cabupdate'),
    url(r'^wsrupdate', sql.wsrupdate, name='wsrupdate'),
    url(r'^userupdate', sql.userupdate, name='userupdate'),

    url(r'^Yesupdate', net.Yesupdate, name='Yesupdate'),
    url(r'^channelupdate', net.channelupdate, name='channelupdate'),
    url(r'^srupdate', net.srupdate, name='srupdate'),
    url(r'^userdate', net.userdate, name='userdate'),

    url(r'^fibre', sql.addfibre, name='fibre'),
    url(r'^ach', sql.addch, name='ach'),
    url(r'^usadd', sql.usadd, name='usadd'),

    url(r'^loadd', views.loadd, name='loadd'),
    url(r'^loachanel', views.loachanel, name='loachanel'),
    url(r'^cabload$', views.cabload, name='cabload'),
    url(r'^wsrload$', views.wsrload, name='wsrload'),

    url(r'^Queryfirbe', query.Queryfirbe, name='Queryfirbe'),
    url(r'^QureyCab', query.QureyCab, name='QureyCab'),
    url(r'^QureyChannel', query.QureyChannel, name='QureyChannel'),
    url(r'^QureyWs', query.QureyWs, name='QureyWs'),
    url(r'^QureyUser', query.QureyUser, name='QureyUser'),
    url(r'^QueryLog', query.QueryLog, name='QueryLog'),

    url(r'^downFirbe', net.downFirbe, name='downFirbe'),
    url(r'^downChannel', net.downChannel, name='downChannel'),
    url(r'^downCab', net.downCab, name='downCab'),
    url(r'^daochu', sql.daochu, name='daochu'),
    url(r'^downwsr', net.downwsr, name='downwsr'),
    url(r'^delog', sql.delog, name='delog'),



    url(r'^newuser', net.newuser, name='newuser'),
    url(r'^passwordupdate', net.updatepassword, name='passwordupdate'),
    url(r'^lgcat', views.lgcat, name='lgcat'),
    url(r'^search', views.search, name='search'),
    url(r'^Chdaochu', sql.Chdaochu, name='Chdaochu'),
    url(r'^Fiechu', sql.Fiechu, name='Fiechu'),
    url(r'^cadao', sql.cadao, name='cadao'),
    url(r'^bodao', sql.bodao, name='bodao'),

]
