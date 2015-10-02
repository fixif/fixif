package test_c is
	function sum_c (i : integer) return integer;
	attribute foreign of sum_c : function is "VHPIDIRECT sum_c";
end test_c;

package body test_c is
	function sum_c (i : integer) return integer is
	begin
		assert false severity failure;
	end sum_c;
end test_c;
