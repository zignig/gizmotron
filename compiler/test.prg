: program
    test as _word
    next <- @test
    : setup
        counter as int
        delay as int
    ;
    : run
        counter <- 2
        delay <- 100
    ;
    : shutdown 
        led <- testing
    ;
    : main 
        setup
        run
        shutdown
    ;
;
