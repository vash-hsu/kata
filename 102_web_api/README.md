#Designing RESTful APIs

* RESTful API hosting by Python (flask)
 * reference: http://blog.luisrei.com/articles/flaskrest.html
--

== for query  

##GET /api/v1/resource
* return JSON to tell object list
 * (pass) test_api_v1_api_get_all_elements_list
##GET /api/v1/resource/resource-id
* return JSON to tell object's value
 * (pass) test_api_v1_api_get_element_by_id
 * (pass) test_api_v1_api_get_element_by_not_found_id

== for update  

##PUT /resource/resource-id
* use new content to replace old item
* return JSON to tell result
 * (pass) test_api_v1_put_by_existent_id
 * (pass) test_api_v1_put_disallow_nonexistent_id

== for add/change  

##POST /resource
* add item to resource
* return JSON to tell result
 * (pass) test_api_v1_post_by_creating_new_id_without_slash
 * (pass) test_api_v1_post_by_creating_new_id_with_slash

== for delete  

##DELETE /resource/resource-id
* delete item from resource
* return JSON to tell result
 * (pass) test_api_v1_post_then_delete
 * (pass) test_api_v1_delete_disallow_nonexistent_id
 * (pass) test_api_v1_delete_disallow_action_without_id


== to do

* (tba) Web Interface and Test Kit
* (tba) Android App to Interact with Web API