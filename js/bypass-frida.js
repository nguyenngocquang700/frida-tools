function hook_pthread_create(){
    var pt_create_func = Module.findExportByName(null,'pthread_create');
    var detect_frida_loop_addr = null;
    console.log('pt_create_func:',pt_create_func);
 
   Interceptor.attach(pt_create_func,{
       onEnter:function(){
           if(detect_frida_loop_addr == null)
           {
                var base_addr = Module.getBaseAddress('libnative-lib.so');
                if(base_addr != null){
                    detect_frida_loop_addr = base_addr.add(0x0000000000000F74)
                    console.log('this.context.x2: ', detect_frida_loop_addr , this.context.x2);
                    if(this.context.x2.compare(detect_frida_loop_addr) == 0) {
                        hook_anti_frida_replace(this.context.x2);
                    }
                }
 
           }
 
       },
       onLeave : function(retval){
        //    console.log('retval',retval);
       }
   })
}
function hook_anti_frida_replace(addr){
    console.log('replace anti_addr :',addr);
    Interceptor.replace(addr,new NativeCallback(function(a1){
        console.log('replace success');
        return;
    },'pointer',[]));
 
}

setImmediate(hook_pthread_create());