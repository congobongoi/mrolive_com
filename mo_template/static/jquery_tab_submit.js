;
jQuery.noConflict();
(function ($) {
	$(document).ready(function(e) {
		// CREATE VARIABLE TO HOLD THE FORM OBJECT
		var piForm = $("#pi_form");
		var laborForm = $("#labor_form");
		var teardownForm = $("#teardown_form");
		var locForm = $("#loc_form");
		var vendorForm = $("#vendor_form");
		var splitForm = $("#split_ro_form");
		var baseForm = $("#base_form");
		var reserveForm = $("#reserve_form");
		var requestForm = $("#request_form");
		var toolsForm = $("#tools_form");
		var mgmtForm = $("#mgmt_form");
		var updateForm = $("#update_form");
		var updMgmtForm = $("#upd_mgmt_form");
		var clearForm = $("#clear_formage");
		var clearCartForm = $("#clear_cart_form");
		var bomSchedForm = $("#bom_sched_form");
		var location_input = '';
	    var $form = $(this);
		var currentBoxNumber = 0;

				function ConfirmDialog(message) {
				  $('<div></div>').appendTo('body')
					.html('<div><h6>' + message + '?</h6></div>')
					.dialog({
					  modal: true,
					  title: 'Confirm',
					  zIndex: 10000,
					  autoOpen: true,
					  width: 'auto',
					  resizable: false,
					  buttons: {
						Yes: function() {
						  // $(obj).removeAttr('onclick');                                
						  // $(obj).parents('.Parent').remove();

						  console.log('clearing cart...');
						  clearCartForm.submit();

						  $(this).dialog("close");
						},
						No: function() {
						  //$('body').append('<h1>Confirm Dialog Result: <i>No</i></h1>');

						  $(this).dialog("close");
						}
					  },
					  close: function(event, ui) {
						$(this).remove();
					  }
					});
				};
	    //ONCHANGE value in user_id field
		updMgmtForm.on("change", "#user_id", function(evt){		
			evt.preventDefault();
			//console.log('submitting user...');
			updateMgmtForm.submit();
		});
		$("#button1_toggle").click(function(evt) { evt.preventDefault; console.log('you clicked it!'); $("#row1_toggle").toggle(1000); });
		$("#button2_toggle").click(function(evt) { evt.preventDefault; $("#row2_toggle").toggle(1000); });	
		splitForm.onsubmit = function(evt){			  
			evt.preventDefault();
			splitForm.submit();
			if ($form.data('submitted') === true) {
				alert("SUBMITTING FORM VIA UPDATE BUTTON TAB OR ENTER!");
				// Previously submitted - don't submit again
				evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
			} 
			else {
				// Mark it so that the next submit can be ignored
				$form.data('submitted', true);
			}				
		};
		//TAB OR ENTER ON THE LOC_INPUT FIELD TO SUBMIT
		splitForm.on("keydown", "#quantity", function(evt){	
            var charCode = evt.keyCode || e.which;			
			if(charCode == 9 || charCode == 13){			
				evt.preventDefault();
				splitForm.submit();
				if ($form.data('submitted') === true) {
					alert("SUBMITTING FORM VIA UPDATE BUTTON ALREADY!");
					// Previously submitted - don't submit again
					evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
				} 
				else {
					// Mark it so that the next submit can be ignored
					$form.data('submitted', true);
				}
            }				
		});
        //		
		vendorForm.onsubmit = function(evt){			  
		    var vend_input = $("#vend_input").val();
			vendor_input = $("#vendor_input").val(vend_input);
			evt.preventDefault();
			vendorForm.submit();
			if ($form.data('submitted') === true) {
				alert("SUBMITTING FORM VIA UPDATE BUTTON TAB OR ENTER!");
				// Previously submitted - don't submit again
				evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
			} 
			else {
				// Mark it so that the next submit can be ignored
				$form.data('submitted', true);
			}				
		};
		//TAB OR ENTER ON THE LOC_INPUT FIELD TO SUBMIT
		vendorForm.on("keydown", "#vend_input", function(evt){	
            var charCode = evt.keyCode || e.which;			
			if(charCode == 9 || charCode == 13){			
				evt.preventDefault();
				vendorForm.submit();
				if ($form.data('submitted') === true) {
					alert("SUBMITTING FORM VIA UPDATE BUTTON ALREADY!");
					// Previously submitted - don't submit again
					evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
				} 
				else {
					// Mark it so that the next submit can be ignored
					$form.data('submitted', true);
				}
            }				
		});
		
		//TAB OR ENTER ON THE LOC_INPUT FIELD TO SUBMIT
		locForm.on("keydown", "#loc_input", function(evt){
            var charCode = evt.keyCode || e.which;			
			if(charCode == 9 || charCode == 13){	
				evt.preventDefault();
				locForm.submit();
				if ($form.data('submitted') === true) {
					alert("SUBMITTING FORM VIA UPDATE BUTTON ALREADY!");
					// Previously submitted - don't submit again
					evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
				} else {
					// Mark it so that the next submit can be ignored
					$form.data('submitted', true);
				}
			}			
		});
		//TAB IN THE 'update' BUTTON TO SUBMIT
		baseForm.on("keydown", "#wo_update", function(evt){
			// GET THE KEY THAT WAS PRESSED
			var charCode = evt.keyCode || e.which;   
			// YOU MAY LOG THE RESULT TO THE CONSOLE TO CONFIRM...
			//console.log(charCode);
			// IF THE KEY IS THE ENTER(13) OR TAB(9) KEY
			// SIMPLY SUBMIT THE FORM....
			if(charCode == 9 || charCode == 13){
				evt.preventDefault();
				// SUBMIT THE FORM....
				//alert("SUBMITTING FORM VIA BUTTON TAB OR ENTER!");
				baseForm.submit();
				if ($form.data('submitted') === true) {
				  alert("SUBMITTING FORM VIA UPDATE BUTTON TAB OR ENTER!");
				  // Previously submitted - don't submit again
				  evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
				} else {
				  // Mark it so that the next submit can be ignored
				  $form.data('submitted', true);
				}				
			}
		});
		//TAB IN THE 'update' BUTTON TO SUBMIT
		baseForm.on("keydown", "#update", function(evt){
			// GET THE KEY THAT WAS PRESSED
			var charCode = evt.keyCode || e.which;   
			// YOU MAY LOG THE RESULT TO THE CONSOLE TO CONFIRM...
			//console.log(charCode);
			// IF THE KEY IS THE ENTER(13) OR TAB(9) KEY
			// SIMPLY SUBMIT THE FORM....
			if(charCode == 9 || charCode == 13){
				evt.preventDefault();
				// SUBMIT THE FORM....
				//alert("SUBMITTING FORM VIA BUTTON TAB OR ENTER!");
				baseForm.submit();
				if ($form.data('submitted') === true) {
				  alert("SUBMITTING FORM VIA UPDATE BUTTON TAB OR ENTER!");
				  // Previously submitted - don't submit again
				  evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
				} else {
				  // Mark it so that the next submit can be ignored
				  $form.data('submitted', true);
				}				
			}
		});
		
		//TAB IN THE wo_number FIELD TO SUBMIT
		baseForm.on("keydown", "#wo_number", function(evt){
			// GET THE KEY THAT WAS PRESSED
			var charCode = evt.keyCode || e.which;   
			// YOU MAY LOG THE RESULT TO THE CONSOLE TO CONFIRM...
			console.log(charCode);
			// IF THE KEY IS THE ENTER(13) OR TAB(9) KEY
			// SIMPLY SUBMIT THE FORM....
			if(charCode == 9 || charCode == 13){
				evt.preventDefault();
				// SUBMIT THE FORM....				
				baseForm.submit(); 
				if ($form.data('submitted') === true) {
				  alert("SUBMITTING FORM VIA WO_NUMBER TAB OR ENTER!");
				  // Previously submitted - don't submit again
				  evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
				} else {
				  // Mark it so that the next submit can be ignored
				  $form.data('submitted', true);
				}				
			}
		});
		//TAB IN THE quantity FIELD TO SUBMIT
		baseForm.on("keydown", "#quantity", function(evt){
			// GET THE KEY THAT WAS PRESSED
			var charCode = evt.keyCode || e.which;   
			// YOU MAY LOG THE RESULT TO THE CONSOLE TO CONFIRM...
			//console.log(charCode);
			// IF THE KEY IS THE ENTER(13) OR TAB(9) KEY
			// SIMPLY SUBMIT THE FORM....
	        if(charCode == 9 || charCode == 13){
				////console.log($('#quantity').val())
				evt.preventDefault();
				// SUBMIT THE FORM...				
				baseForm.submit(); 
				//$("#stock_label").focus();
				if ($form.data('submitted') === true) {
				  alert("ALREADY SUBMITTING FORM VIA QUANTITY TAB OR ENTER!");
				  // Previously submitted - don't submit again
				  evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
				} else {
				  // Mark it so that the next submit can be ignored
				  $form.data('submitted', true);
				}				
			}
		});
		requestForm.on("keydown", "#notes", function(evt){
			// GET THE KEY THAT WAS PRESSED
			var charCode = evt.keyCode || e.which;   
			// YOU MAY LOG THE RESULT TO THE CONSOLE TO CONFIRM...
			//console.log(charCode);
			// IF THE KEY IS THE ENTER(13) OR TAB(9) KEY
			// SIMPLY SUBMIT THE FORM....
	        if(charCode == 9 || charCode == 13){
				////console.log($('#quantity').val())
				evt.preventDefault();
				// SUBMIT THE FORM...				
				baseForm.submit(); 
				//$("#stock_label").focus();
				if ($form.data('submitted') === true) {
				  alert("ALREADY SUBMITTING FORM VIA QUANTITY TAB OR ENTER!");
				  // Previously submitted - don't submit again
				  evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
				} else {
				  // Mark it so that the next submit can be ignored
				  $form.data('submitted', true);
				}				
			}
		});
		requestForm.on("keydown", "#request_submit", function(evt){
			// GET THE KEY THAT WAS PRESSED
			var charCode = evt.keyCode || e.which;   
			// YOU MAY LOG THE RESULT TO THE CONSOLE TO CONFIRM...
			//console.log(charCode);
			// IF THE KEY IS THE ENTER(13) OR TAB(9) KEY
			// SIMPLY SUBMIT THE FORM....
	        if(charCode == 9 || charCode == 13){
				////console.log($('#quantity').val())
				evt.preventDefault();
				// SUBMIT THE FORM...				
				baseForm.submit(); 
				//$("#stock_label").focus();
				if ($form.data('submitted') === true) {
				  alert("ALREADY SUBMITTING FORM VIA QUANTITY TAB OR ENTER!");
				  // Previously submitted - don't submit again
				  evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
				} else {
				  // Mark it so that the next submit can be ignored
				  $form.data('submitted', true);
				}				
			}
		});
		piForm.on("keydown", "#no_quantity", function(evt){
			// GET THE KEY THAT WAS PRESSED
			var charCode = evt.keyCode || e.which;   
			if(charCode == 9 || charCode == 13){
				evt.preventDefault();
				// SUBMIT THE FORM...				
				piForm.submit(); 
				if ($form.data('submitted') === true) {
				  alert("ALREADY SUBMITTING FORM VIA QUANTITY TAB OR ENTER!");
				  // Previously submitted - don't submit again
				  evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
				} 
				else {
				  // Mark it so that the next submit can be ignored
				  $form.data('submitted', true);
				}				
			}
		});
		toolsForm.on("change", ".mode_selector", function(evt){
			//set all other field's values to zero except user_id
			//$('#user_id').val('');
			$('#wo_task').val('');
			var active_mode = $('input[name="mode_selector"]:checked').val();
			$('#sel_mode').val(active_mode);			
			evt.preventDefault();			
			clearForm.submit();
		});		    
		
       //ONCHANGE value in label field
		//reserveForm.on("keydown", "#wo_number", function(evt){
        //    evt.preventDefault();		
		//});
       //ONCHANGE value in label field
		//reserveForm.on("keydown", "#wo_task", function(evt){
        //    evt.preventDefault();			
		//});
       //ONCHANGE value in label field
		//reserveForm.on("keydown", "#label", function(evt){
        //    evt.preventDefault();		
		//});
		
	    reserveForm.on('keyup keypress', function(evt) {  
			var charCode = evt.keyCode || e.which;   
			if(charCode == 13){			
				evt.preventDefault();
				if ($('#quantity').is(':focus')){
                    //$('#quantity').val('');					
					//$('wo_number').val('');
					//$('wo_task').val('');
					//$('label').val('');
					reserveForm.submit();
					if ($form.data('submitted') === true) {
					  alert("ALREADY SUBMITTING FORM VIA QUANTITY TAB OR ENTER!");
					  // Previously submitted - don't submit again
					  evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
					} 
					else {
					  // Mark it so that the next submit can be ignored
					  $form.data('submitted', true);
					}
				}
            }				
		});
		
		laborForm.on("change", "#mode_selector", function(evt){
			//set all other field's values to zero except user_id
			//$('#user_id').val('');
			$('#wo_number').val('');
			var active_mode = $('#mode_selector').find(":selected").val();
			$('#sel_mode').val(active_mode);		
			evt.preventDefault();			
			clearForm.submit();
		});
		
        //ONCHANGE value in mode_selector field
		requestForm.on("change", "#mode_selector", function(evt){
			//set all other field's values to zero except user_id
			//console.log("mode change.");
			$('#notes').val('');
			$('#wo_number').val('');
			$('#wo_task').val('');
			$('#quantity').val('');
			$('#part_number').val('');
			$('#wo_task').trigger('focus');
			//var active_mode = $('input[name="mode_selector"]:checked').val();
			var active_mode = $('#mode_selector').find(":selected").val();
			$('#sel_mode').val(active_mode);		
			evt.preventDefault();			
			clearForm.submit();
		});
		
        //ONCHANGE value in mode_selector field
		reserveForm.on("change", "#mode_selector", function(evt){
			//set all other field's values to zero except user_id
			//console.log("mode change.");
			$('#label').val('');
			$('#wo_number').val('');
			$('#wo_task').val('');
			$('#quantity').val('');
			$('#label').trigger('focus');
			//var active_mode = $('input[name="mode_selector"]:checked').val();
			var active_mode = $('#mode_selector').find(":selected").val();
			$('#sel_mode').val(active_mode);		
			evt.preventDefault();			
			clearForm.submit();
		});
		
        //ONCHANGE value in mode_selector field
		baseForm.on("change", "#mode_selector", function(evt){
			//set all other field's values to zero except user_id
			$('#rack').val('');
			$('#location').val('');
			$('#warehouse').val('');
			$('#wo_number').val('');
			//var active_mode = $("input[name='mode_selector[]']").attr('value')
			var active_mode = $('#mode_selector').find(":selected").val();
			//console.log(' - active mode: ' + active_mode);
			$('#sel_mode').val(active_mode);
			$('#cart_code').val(active_mode);
			//user_name = $('#user_name').val();
			//('#user_logged').val(user_name);
			if (active_mode == '2') {
				$('div[id="record_input"]').attr('style','visibility:hidden;');
				//console.log('just hid it!');
		    }
			else if (active_mode == '1' || active_mode == '3') {
				$('div[id="record_input"]').attr('style','visibility:visible;');
				//console.log('just unhid it!');
		    }			
			evt.preventDefault();			
			clearForm.submit();
		});
		
        //ONCHANGE value in user_id field
		updateForm.on("change", "#user_id", function(evt){
			//set all other field's values to zero except user_id			
			var active_amode = $('#active_mode').val();
			var user_id = $('#user_id').val();
			//console.log(user_id);
			if (user_id != '') {
			    $('#user_logged').val(user_id);
                user_name = $("input[type=password][id='user_id']").attr('disp-name');
                $('#user_name').val(user_name);	
		    }
            ////console.log(user_name);	
            if (active_mode) {
				if (user_id) {
					$('#show_all').val('1');
			    }
				else {
					$('#show_all').val('0');
					////console.log('hide all.');
				}
            }
            else {
				$('#show_all').val('0');
				////console.log('hide all fields');
			}			
		    //console.log('submitting user_id');			
			evt.preventDefault();
			updateForm.submit();
		});
		
        //ONCHANGE value in user_id field
		baseForm.on("change", "#user_id", function(evt){
			//set all other field's values to zero except user_id			
			var active_mode = $('#mode_selector').val();			
			var user_id = $('#user_id').val();
			//console.log(user_id + '...submitting...');			
			evt.preventDefault();
			baseForm.submit();
		});
       //ONCHANGE value in user_id field
		piForm.on("change", "#user_id", function(evt){
			var user_id = $('#user_id').val();
			//console.log(user_id);
			if (user_id != '') {
			    $('#user_logged').val(user_id);
                user_name = $("input[type=password][id='user_id']").attr('disp-name');
                $('#user_name').val(user_name);	
		    }		
			evt.preventDefault();
			piForm.submit();
		});

       //ONCHANGE value in user_id field
		toolsForm.on("change", "#user_id", function(evt){	
            //console.log('Yay');		
			evt.preventDefault();
			toolsForm.submit();
		});
		
       //ONCHANGE value in user_id field
		laborForm.on("change", "#user_id", function(evt){	
            $("#search_user").val("T");
			//search_user = $("#search_user").val();
            //console.log(search_user); 			
			evt.preventDefault();
			laborForm.submit();
		});
		
       //ONCHANGE value in user_id field
		toolsForm.on("keydown", "#label", function(evt){	
            //console.log('Label');		
			var charCode = evt.keyCode || e.which;   
			// YOU MAY LOG THE RESULT TO THE CONSOLE TO CONFIRM...
			////console.log(charCode);
			// IF THE KEY IS THE ENTER(13) OR TAB(9) KEY
			// SIMPLY SUBMIT THE FORM....
			if(charCode == 9 || charCode == 13){
				evt.preventDefault();
				// SUBMIT THE FORM....				
				toolsForm.submit(); 
				$('#label').val('');	
				if ($form.data('submitted') === true) {
				  alert("SUBMITTING FORM VIA WO_NUMBER TAB OR ENTER!");
				  // Previously submitted - don't submit again
				  evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
				} else {
				  // Mark it so that the next submit can be ignored
				  $form.data('submitted', true);
				}				
			}
		});
		
		//TAB IN THE wo_number FIELD TO SUBMIT
		laborForm.on("keydown", "#wo_number", function(evt){
			// GET THE KEY THAT WAS PRESSED
			var charCode = evt.keyCode || e.which;   
			// YOU MAY LOG THE RESULT TO THE CONSOLE TO CONFIRM...
			////console.log(charCode);
			// IF THE KEY IS THE ENTER(13) OR TAB(9) KEY
			// SIMPLY SUBMIT THE FORM....
			if(charCode == 9 || charCode == 13){
				evt.preventDefault();
				// SUBMIT THE FORM....				
										  
										 
					  
											  
				laborForm.submit(); 
				if ($form.data('submitted') === true) {
				  alert("SUBMITTING FORM VIA WO_NUMBER TAB OR ENTER!");
				  // Previously submitted - don't submit again
				  evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
				} else {
				  // Mark it so that the next submit can be ignored
				  $form.data('submitted', true);
				}				
			}
		});
		
        //ONSUBMIT OF CLEAR CART FORM
		baseForm.on("change", "#rack", function(evt){
            ////console.log('rack entered: ');			
			var cart_code = $('#rack').val();
			$('#cart_code').val(cart_code);	
            ////console.log(cart_code);
		});
		clearCartForm.on("submit", "#clear_cart", function(evt){
            //console.log('rack entered: ');			
			var cart_code = $('#rack').val();
			$('#cart_code').val(cart_code);
            var record = $('#wo_number').val();
            $('#stock_label').val(record);			
            ////console.log(record);
			evt.preventDefault();
			ConfirmDialog('Are you sure you want to clear the cart?');
			//clearCartForm.submit();
		});
	    updateForm.on('keyup keypress', function(evt) {
		  var keyCode = evt.keyCode || e.which;
		  if (keyCode === 13) { 
			evt.preventDefault();
		  }
        });		
	    updMgmtForm.on('keyup keypress', function(evt) {
		  var keyCode = evt.keyCode || e.which;
		  if (keyCode === 13) { 
			evt.preventDefault();
			 if ($('rank').is(':focus') || $('due_date').is(':focus') || $('manager').is(':focus')) {
				updMgmtForm.submit();
			 }
			}
        });
	    piForm.on('keyup keypress', function(evt) {
		  var keyCode = evt.keyCode || e.which;
		  if (keyCode === 13) { 
			evt.preventDefault();
			if ($('no_quantity').is(':focus')) {
				piForm.submit();
            }				 
		  }
        });
	    toolsForm.on('keyup keypress', function(evt) {
		  var keyCode = evt.keyCode || e.which;
		  if (keyCode === 13) { 
			evt.preventDefault();
			if ($('label').is(':focus')) {
				toolsForm.submit();
            }				 
			$('label').val('');
			$('wo_task').val('');
		  }
        });
	    locForm.on('keyup keypress', function(evt) {
		  var keyCode = evt.keyCode || e.which;
		  if (keyCode === 13) { 
			evt.preventDefault();
			if ($('loc_input').is(':focus')) {
				locForm.submit();
            }				 
		  }
        });
	    teardownForm.on('keyup keypress', function(evt) {
		  var keyCode = evt.keyCode || e.which;
		  if (keyCode === 13) { 
			evt.preventDefault();
			  if ($('#quantity').is(':focus') || $('#serial_number').is(':focus') || $('#notes').is(':focus')) {
					teardownForm.submit();
			  }
		    }
        });
		
		//TAB IN THE 'update' BUTTON TO SUBMIT
		laborForm.on("keydown", "#labor_submit", function(evt){
			// GET THE KEY THAT WAS PRESSED
			var charCode = evt.keyCode || e.which;   
			// YOU MAY LOG THE RESULT TO THE CONSOLE TO CONFIRM...
			//console.log(charCode);
			// IF THE KEY IS THE ENTER(13) OR TAB(9) KEY
			// SIMPLY SUBMIT THE FORM....
			if(charCode == 9 || charCode == 13){
				evt.preventDefault();
				// SUBMIT THE FORM....
				//alert("SUBMITTING FORM VIA BUTTON TAB OR ENTER!");
				baseForm.submit();
				if ($form.data('submitted') === true) {
				  alert("SUBMITTING FORM VIA UPDATE BUTTON TAB OR ENTER!");
				  // Previously submitted - don't submit again
				  evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
				} else {
				  // Mark it so that the next submit can be ignored
				  $form.data('submitted', true);
				}				
			}
		});

		//TAB IN THE 'update' BUTTON TO SUBMIT
		laborForm.on("keydown", "#task_submit", function(evt){
			// GET THE KEY THAT WAS PRESSED
			var charCode = evt.keyCode || e.which;   
			// YOU MAY LOG THE RESULT TO THE CONSOLE TO CONFIRM...
			//console.log(charCode);
			// IF THE KEY IS THE ENTER(13) OR TAB(9) KEY
			// SIMPLY SUBMIT THE FORM....
			if(charCode == 9 || charCode == 13){
				evt.preventDefault();
				// SUBMIT THE FORM....
				//alert("SUBMITTING FORM VIA BUTTON TAB OR ENTER!");
				baseForm.submit();
				if ($form.data('submitted') === true) {
				  alert("SUBMITTING FORM VIA UPDATE BUTTON TAB OR ENTER!");
				  // Previously submitted - don't submit again
				  evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
				} else {
				  // Mark it so that the next submit can be ignored
				  $form.data('submitted', true);
				}				
			}
		});
		
		laborForm.on("submit", "#task_submit", function(evt){
			// submit more than once return false
			//console.log('submitting wo_update...')
			evt.preventDefault();
			// SUBMIT THE FORM...				
			laborForm.submit();
			$('#wo_number').val('');
            $('#batch_recall').val('');			
			if ($form.data('submitted') === true) {
			  alert("ALREADY SUBMITTING.  PLEASE WAIT UNTIL PAGE FINISHES LOADING TO SUBMIT AGAIN.");
			  // Previously submitted - don't submit again
			  evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
			} 
			else {
			  // Mark it so that the next submit can be ignored
			  $form.data('submitted', true);
			}
		});
		
		laborForm.on("submit", "#labor_submit", function(evt){
			// submit more than once return false
			//console.log('submitting wo_update...')
			evt.preventDefault();

			// SUBMIT THE FORM...				
			laborForm.submit();	
			$('#wo_number').val('');
            $('#batch_recall').val('');			
			if ($form.data('submitted') === true) {
			  alert("ALREADY SUBMITTING.  PLEASE WAIT UNTIL PAGE FINISHES LOADING TO SUBMIT AGAIN.");
			  // Previously submitted - don't submit again
			  evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
			} 
			else {
			  // Mark it so that the next submit can be ignored
			  $form.data('submitted', true);
			}
		});
		
		baseForm.on("submit", "#wo_update", function(evt){
			// submit more than once return false
			//console.log('submitting wo_update...')
			evt.preventDefault();
			// SUBMIT THE FORM...				
			baseForm.submit();	 
			if ($form.data('submitted') === true) {
			  alert("ALREADY SUBMITTING.  PLEASE WAIT UNTIL PAGE FINISHES LOADING TO SUBMIT AGAIN.");
			  // Previously submitted - don't submit again
			  evt.preventDefault ? evt.preventDefault() : (evt.returnValue = false);
			} 
			else {
			  // Mark it so that the next submit can be ignored
			  $form.data('submitted', true);
			}
		});
	});
})(jQuery);