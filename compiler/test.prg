// comment
: hello


status as bit
data as word

r <- 2 
j <- 2 
: whence ;
: init on runner off;
: unit ;
: name test 20  ;
: meta num num num ;

bob as meta

: test
	r <- @test
;

: on 
	button1 <- true
;

: off 
	button2 <- false
;

: runner
	run <- true
	@rwr
	@blag
	bit
	evac
	: one ;

;

: reboot ; 
: testing; 
: build a over test ; 
init

;
