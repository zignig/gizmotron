: hello

r <- 2 
j <- 2 
: whence ;
: init @test @gorf ;
: unit ;
: num as 16b ; 
: name test 20  ;
: meta num num num ;

bob as meta

: test
	a <- 4
	b <- 5
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

init

;
