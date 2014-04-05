/*
 *     Copyright (c) 2013 CoNWeT Lab., Universidad Politécnica de Madrid
 *
 *     This file is part of the simple-history-module2-linear-graph operator.
 *
 *     simple-history-module2-linear-graph is free software: you can redistribute it and/or modify
 *     it under the terms of the GNU Affero General Public License as published
 *     by the Free Software Foundation, either version 3 of the License, or (at
 *     your option) any later version.
 *
 *     simple-history-module2-linear-graph is distributed in the hope that it will be useful, but
 *     WITHOUT ANY WARRANTY; without even the implied warranty of
 *     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero
 *     General Public License for more details.
 *
 *     You should have received a copy of the GNU Affero General Public License
 *     along with simple-history-module2-linear-graph. If not, see <http://www.gnu.org/licenses/>.
 *
 *     Linking this library statically or dynamically with other modules is
 *     making a combined work based on this library.  Thus, the terms and
 *     conditions of the GNU Affero General Public License cover the whole
 *     combination.
 *
 *     As a special exception, the copyright holders of this library give you
 *     permission to link this library with independent modules to produce an
 *     executable, regardless of the license terms of these independent
 *     modules, and to copy and distribute the resulting executable under
 *     terms of your choice, provided that you also meet, for each linked
 *     independent module, the terms and conditions of the license of that
 *     module.  An independent module is a module which is not derived from
 *     or based on this library.  If you modify this library, you may extend
 *     this exception to your version of the library, but you are not
 *     obligated to do so.  If you do not wish to do so, delete this
 *     exception statement from your version.
 *
 */

/*develop by Juan Carlos Hdez. (programaando@gmail.com) para CirculoOfij, proyecto Pragmation. */

(function () {

    "use strict";
    
    /* NGSI var */
    var ngsi_subscriptionId = null;
    var ngsi_refresh_interval;
    var ngsi_server;
    var ngsi_proxy;
    var connection = null;
    
    var contador = 1;
    
    var processHistoricData = function processHistoricData(patientId, response) {
        var i, parsedResponse, data, config;

        /* First element is the older.
        if (typeof response.responseText != 'object') {
            parsedResponse = JSON.parse(response.responseText);
        } else {
            parsedResponse = response.responseText;
        }*/

       
              
        // Axis config
        

        MashupPlatform.wiring.pushEvent("OutputStatus", JSON.stringify("RESET"));
        MashupPlatform.wiring.pushEvent("OutputStatus", JSON.stringify("START"));
        
       var config =  {
                bars : {
                    show : true,
                    horizontal : false,
                    shadowSize : 0,
                    barWidth : 0.2
                  },
                  mouse : {
                    track : true,
                    relative : true
                  },
                  yaxis : {
                    min : 0,
                    autoscaleMargin : 1
                  }
                ,
                data: {
                    0: [
                        [
                            1,
                            60
                        ],
                        [
                            2,
                            60
                        ],
                        [
	                         3,
	                         40
                         ]
                    ]
                }};

       
       contador = 4;
       
        MashupPlatform.wiring.pushEvent("OutputStatus", JSON.stringify(config));
       
        //it is refresehed in real time
        //MashupPlatform.wiring.pushEvent("OutputStatus", JSON.stringify('END'));
    };

    // input callback
    var handlerPatientIdInput = function handlerPatientIdInput(patientId, test) {
        if (patientId) {
        	processHistoricData.call(this, patientId, test);
        }
    };
    
    //process new notifications
    var process_entities = function process_entities(data) {
        
    	var info = data;
    	
    	    	
    	var data={data: {
                    0: [
                        [
                            contador,
                            parseFloat(info.elements.JSMG1437.tiempo)
                        ]
                    ]
                }};
    	
    	contador ++;
    	 MashupPlatform.wiring.pushEvent("OutputStatus", JSON.stringify(data));
    	
    };
    
    //Subscription
    var doInitialSubscription = function doInitialSubscription() {

        ngsi_server = MashupPlatform.prefs.get('ngsi_server');
        ngsi_proxy = MashupPlatform.prefs.get('ngsi_proxy');
        
  
         connection = new NGSI.Connection(ngsi_server, {
            ngsi_proxy_url: ngsi_proxy
        });
         
                 
        
        var entityIdList = [
            {type: 'pragmationTime', id: '.*', isPattern: true}
        ];
        var attributeList = ['tiempo'];
        var duration = 'P1M';
        var throttling = null;
        /*var notifyConditions = [{
            type: 'ONTIMEINTERVAL',
            condValues: ['PT10S']
        }];*/
        var notifyConditions = [{
            type: 'ONCHANGE',
            condValues: ['tiempo']
        }];
        
        var options = {
            flat: true,
            onNotify: process_entities,
            onSuccess: function (data) {
                //ngsi_subscriptionId = data.subscriptionId;
                //ngsi_refresh_interval = setInterval(refreshNGSISubscription, 1000 * 60 * 60 * 2);  // each 2 hours
            }
        };
        connection.createSubscription(entityIdList, attributeList, duration, throttling, notifyConditions, options);
    };
    
    MashupPlatform.wiring.registerCallback("PatientIdInput", handlerPatientIdInput.bind(this));

    /* First function to be launched */
    doInitialSubscription();
    
    handlerPatientIdInput('testMode', 1);

})();