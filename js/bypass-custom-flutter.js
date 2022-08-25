// recv(function(msg) {
//     console.log("message:" + msg);
// });
rpc.exports = {
    customFlutter: function (pattern) {
        console.log(pattern)

        Java.perform(function (){
            var m = Process.findModuleByName("libflutter.so");
            //  var pattern = "55 41 57 41 56 41 55 41 54 53 48 81 EC F8 00 00 00 C6 02 50 48 8B 9F A8 00 00 00 48 85 DB"
            // var pattern = "55 41 57 41 56 41 55 41 54 53 48 83 ec 38 c6 02 50 48 8b af a8 00 00 00 48 85 ed 74 6a 48"
            console.log(pattern)
            var res = Memory.scan(m.base, m.size, pattern, {
                onMatch: function (address, size) {
                    console.log('[+] ssl_verify_result found at: ' + address.toString());

                    // Add 0x01 because it's a THUMB function
                    // Otherwise, we would get 'Error: unable to intercept function at 0x9906f8ac; please file a bug'
                    // hook_ssl_verify_result(address.add(0x01));
                    // for 64 bit
                    Interceptor.attach(address, {
                        onEnter: function (args) {
                            console.log("Disabling SSL validation")
                        },
                        onLeave: function (retval) {
                            console.log("Retval: " + retval)
                            retval.replace(0x1);

                        }
                    });

                },
                onError: function (reason) {
                    console.log('[!] There was an error scanning memory');
                },
                onComplete: function () {
                    console.log("All done")
                }
            });
        })
        // setTimeout(a, 1000)
    }
};