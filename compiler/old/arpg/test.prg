def startup(){
    var status int;
    status := 0;
    var counter int;
    counter := 0;
}

def run(){
    counter := counter + 1;
    blink();
}

task go {
    var running int;
    runnint := 1;
    startup();
    while( True ){
        run();
    };
}
 
