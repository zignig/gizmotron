def main(){
    counter := 1 ;
    delay := 12345;
    start();
    run();
    shutdown();
}

def start(){
}

def run(){
    while(runnin == 1){
        go();
    };
}

def shutdown(){
	active := 0;
	if ( running == 0){
		print(b);
	};

}
