setTimeout(function(){
    Java.perform(function (){
        var AFEvent = Java.use("com.appsflyer.internal.ah");
        AFEvent.params.overload().implementation = function(){
            var ret = this.params.overload().call(this);
            const jsonObject = Java.use("org.json.JSONObject");
            let jsonParams = jsonObject.$new(ret);
            console.log(jsonParams.toString());
            return null;
        }
    })
})