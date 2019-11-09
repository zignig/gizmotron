: program
    led := 1
    active := 300 
    counter := 111 
    delay := 6500 
    one := "one"
    other := "test"
    fnord := "this is a test now"

    alphabet := "abcdefghijklmnopqrstuvwxyz"
    : other_code 
        serial_out = alphabet
    ;
    : wait ;
    : setup
        counter = 0
        delay = 65300
    ;
    : run
        blink()
    ;
    : blink led = on ; 
    : shutdown 
        active = false
    ;
    setup()
    run()
    shutdown()
    : go
        setup()
        setup()
        run()
    ;
;
