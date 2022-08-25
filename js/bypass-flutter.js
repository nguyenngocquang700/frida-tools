function hook_ssl_verify_result(address)
{
  Interceptor.attach(address, {
    onEnter: function(args) {
      console.log("Disabling SSL validation")
    },
    onLeave: function(retval)
    {
      console.log("Retval: " + retval)
      retval.replace(0x1);
 
    }
  });
}
function disablePinning()
{
 var m = Process.findModuleByName("libflutter.so"); 
//  var pattern = "55 41 57 41 56 41 55 41 54 53 48 81 EC F8 00 00 00 C6 02 50 48 8B 9F A8 00 00 00 48 85 DB"
 var pattern = "55 41 57 41 56 41 55 41 54 53 48 83 ec 38 c6 02 50 48 8b af a8 00 00 00 48 85 ed 74 6a 48"

 var res = Memory.scan(m.base, m.size, pattern, {
  onMatch: function(address, size){
      console.log('[+] ssl_verify_result found at: ' + address.toString());
     hook_ssl_verify_result(address);
       
    }, 
  onError: function(reason){
      console.log('[!] There was an error scanning memory');
    },
    onComplete: function()
    {
      console.log("All done")
    }
  });
}
setTimeout(disablePinning, 1000)