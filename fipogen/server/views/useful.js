/* Useful javascript functions */

/* build the query from the different input elements of the form named 'form'
(exactly like the serialize function of jQuery, BUT without taking into account the inputs with named beginning by 'except_name') */
function queryString(form, except_name)
{
	var e=$("#"+form)[0].elements;
	var s = [];
	for(var i=0;i<e.length;i++)
	{
		if (e[i].name.substring(0,except_name.length)!= except_name)
		{
			if (e[i].name!="")
				if (e[i].type=="checkbox")
					s.push( e[i].name +"="+(e[i].checked?"yes":"no") );
				else
					s.push( e[i].name+"="+e[i].value );
		}
	}
	return s.join("&");
}

/* function to evaluate and validate a FPF (Q-notation or parentheses-notation) */
var expQ = /^([su]?)Q([+-]?[0-9]+)\.([+-]?[0-9]+)$/;	// Q-notation
var expP = /^([su]?)\(([+-]?[0-9]+),([+-]?[0-9]+)\)$/;	// Parentheses-notation
var lit = "[+-]?\\d+(?:\\.\\d+)?";
var expC = new RegExp( "^"+lit+"$");					// literal constant
var expI = new RegExp( "^\\[("+lit+");("+lit+")\\]$");			// interval
var separators = new Set(["\n", "\t", ",", " "]); 	// text separators

/* check if a string is a valid FPF (Q notation or parentheses) 
 * and return the appropriate error message (or '' if no error) */
function msgValidFPF( fpf)
{
	if (fpf.length<4)
		return 'The FPF is not valid, it should be with Q-notation (like Q3.6 or uQ8.0) or MSB/LSB notation (6,-2)';	
	/* check the Q-notation */
	var resQ = expQ.exec(fpf);
	if ( resQ )
	{
		var wl = parseInt(resQ[2]) + parseInt(resQ[3]);
		if ( (wl>1 && resQ[1]=='u') || (wl>2 && resQ[1]!='u') )
			return '';
		else
			return 'With the Q-notation, the integer part and the fractional part should (like Q3.5 or Q10.-2)'; 
	}
	/* check the parentheses-notation */
	var resP = expP.exec(fpf);
	if ( resP )
	{
		var wl = parseInt(resP[2]) - parseInt(resP[3]) + 1;
		if ( (wl>1 && resP[1]=='u') || (wl>2 && resP[1]!='u') )
			return '';
		else
			return 'With MSB/LSB notation, the MSB should be greater than the LSB (like (5,-3) or (10,-3) )';
	}
	return 'The FPF is not valid, it should be with Q-notation (like Q3.6 or uQ8.0) or MSB/LSB notation (6,-2)';
}

/* verify an FPF input, and set the custom validity message */
function verifyFPF(fpf)
{
	fpf.setCustomValidity( msgValidFPF( fpf.value) );
}

/* check if a string is a valid literal constant or interval
 * and return the appropriate error message (or '' if no error) */
function msgValidConstInterval( ci)
{
	/* check the literal constant */
	if ( expC.test(ci) )
		return '';
	/* check the interval */
	var I = expI.exec(ci);
	if (I)
	{
		if (parseFloat(I[1]) <= parseFloat(I[2]))
			return '';
		else
			return 'For an interval [x;y], the x should be lower than y';
		//TODO: possible problem if lower and upper bounds of the interval arrive on the same double value... ( like [x+eps;x] where eps<ulp(x) )
		//TODO: possible problem with too big/small values (non representable with floating point)
	}
	/* otherwise, failed */
	return 'The literal is not valid, it should be a real constant or an interval (like [-12.5;26.8])';
}


/* verify a Constant_or_interval input, and set the custom validity message */
function verifyConstInterval(ci)
{
	ci.setCustomValidity( msgValidConstInterval( ci.value) );
}

/* verify an FPF_or_wordlength input, and set the custom validity message */
function verifyWL(fpfORwl)
{
	// check for a wordlength (integer >2)
	var msgWL = '';
	if ( isNaN(+fpfORwl.value) )
		msgWL = 'This should be an integer greater than 1, or a Fixed-Point Format (Q-notation or MSB/LSB notation)';
	else if (parseInt(fpfORwl.value) != +fpfORwl.value)
		msgWL = 'A wordlength should be an integer';
	else if (+fpfORwl.value<2)
		msgWL = 'A wordlength should be greater than 1';
	// mix FPF validity message and wordlength validity message
	fpfORwl.setCustomValidity ( msgWL );
}
function verifyFPF(FPF)
{
	FPF.setCustomValidity(msgValidFPF( FPF.value))
}

function processDiv(text)
{
	var ci_s = [];
	var str = "";
	ci_s= text.split("\n");
	return ci_s;

}
