: program
    active as bool
    counter as int
    delay as int
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
;
