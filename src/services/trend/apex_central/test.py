def payload(domain_type,content_filter):
    #domain_type = print(input("Ingrese dominio: " ))
    #content_filter = print(input("Ingrese filtro: "))

    payload = str("?type=" + domain_type + "&contentFilter=" + content_filter)
    payload1 = str("prueba")
    print(payload)

payload("asd","asd")