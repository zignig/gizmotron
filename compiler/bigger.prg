: program
    active as 300 
    counter as 111 
    delay as "testing" 
    one as "one"
    fnord as "this is a test now"
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
