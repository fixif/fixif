package bidon is
	function sum (i : integer) return integer;
	attribute foreign of sum : function is "VHPIDIRECT sum";
end bidon;

package body bidon is
	function sum (i : integer) return integer is
	begin
		assert false severity failure;
	end sum;
end bidon;
