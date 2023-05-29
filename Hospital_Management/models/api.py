import xmlrpc.client

url = 'http://127.0.0.1:8015'
db = 'learn'
username = 'admin'
password = 'admin'

# authentication
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

uid = common.authenticate(db, username, password, {})

if uid:
    print("authenticate succeeded")
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    # # search method
    # partners = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]],
    #                              {'limit': 7})
    # partners_count = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[['is_company', '=', True]]])
    # print("partners_count = ", partners_count)
    #
    # # read method
    # partners_rec = models.execute_kw(db, uid, password, 'res.partner', 'read', [partners], {'fields': ['id', 'name']})
    #
    # # search read
    # partners_rec2 = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['is_company', '=', True]]],
    #                                   {'fields': ['id', 'name']})
    # # print("---->", partners_rec2)
    #
    # vals = {
    #     'name': "basem waled",
    #     'email': "basem@mail.com"
    # }
    #
    # created_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [vals])
    # print("created record ->", created_id)

    # partners = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['email', '=', 'basem@mail.com']]])

    # models.execute_kw(db, uid, password, 'res.partner', 'write', [partners, {'mobile': "22222", 'phone': "1234567891"}])

    models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[46]])

else:
    print("authentication failed")
