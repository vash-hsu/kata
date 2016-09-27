package com.blogspot.rulesare.restapiclientdemo;

import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;
import android.content.Context;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;


// for http request, rest api and json

import java.io.IOException;
import java.net.URL;
import java.util.Arrays;


public class MainActivity extends AppCompatActivity {

    private Spinner my_spinner;
    private Context my_context;
    ArrayAdapter<String> my_adapter;

    private Button button2put;
    private Button button2post;
    private Button button2delete;
    private Button button2reset;

    private EditText edittext_rid;
    private EditText edittext_json;
    private EditText edittext_ip;
    private EditText edittext_port;

    String[] arraySpinner;
    String[] arrayTesting;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        arraySpinner = new String[1];
        arraySpinner[0] = String.valueOf("... new ...");
        initialize_gui();
    }

    private void initialize_gui()
    {
        Log.d("DM: initialize_gui", "... ");
        _initialize_edittext();
        _initialize_button();
        _initialize_spinner();
        draw_gui();
    }

    private void clean_gui()
    {
        Log.d("DM: clean_gui", "... ");
        // ready for creation new
        edittext_rid.setText("");
        edittext_json.setText("{\n\n}");
        my_spinner.setSelection(0);
        button2put.setVisibility(View.VISIBLE);
        button2post.setVisibility(View.INVISIBLE);
        button2delete.setVisibility(View.INVISIBLE);
        button2reset.setVisibility(View.VISIBLE);
    }

    private void _initialize_edittext()
    {
        Log.d("DM: _initialize_edittext", "... ");
        edittext_rid = (EditText) findViewById(R.id.edittext_rid);
        edittext_json = (EditText) findViewById(R.id.edittext_json);
        edittext_ip = (EditText) findViewById(R.id.edittext_ip);
        edittext_port = (EditText) findViewById(R.id.edittext_port);
    }

    private void _initialize_button()
    {
        Log.d("DM: _initialize_button", "... ");
        button2put = (Button) findViewById(R.id.button2put);
        button2post = (Button) findViewById(R.id.button2post);
        button2delete = (Button) findViewById(R.id.button2delete);
        button2reset = (Button) findViewById(R.id.button2reset);
        button2put.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) { action_for_button(button2put); } });
        button2post.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) { action_for_button(button2post); } });
        button2delete.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) { action_for_button(button2delete); } });
        button2reset.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) { action_for_button(button2reset); } });
    }

    private void _initialize_spinner()
    {
        Log.d("DM: _initialize_spinner", "... ");
        my_spinner = (Spinner) findViewById(R.id.spinner);
        my_context = this.getApplicationContext();
        my_adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, arraySpinner);
        my_adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        my_spinner.setAdapter(my_adapter);
        my_spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener()
        {
            @Override
            public void onItemSelected(AdapterView<?> arg0, View arg1, int position, long arg3) {
                action_for_spinner_selected(position);
            }
            @Override
            public void onNothingSelected(AdapterView<?> arg0) {
                Log.d("onCreate", "onNothingSelected");
                action_for_spinner_nothing_selected();
            }
        });
    }

    private void draw_gui()
    {
        Log.d("DM: draw_gui", "...");
        clean_gui();
        draw_spinner();
    }

    public void callback_draw_spinner(String[] string_array)
    {
        if (string_array == null) // no list
        {
            arrayTesting = new String[1];
            arrayTesting[0] = String.valueOf("... new ...");
            arraySpinner = arrayTesting;
            my_adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, arraySpinner);
            my_adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
            my_spinner.setAdapter(my_adapter);
        }
        else
        {
            arrayTesting = new String[string_array.length+1];
            arrayTesting[0] = String.valueOf("... new ...");
            System.arraycopy(string_array, 0, arrayTesting, 1, string_array.length);
            arraySpinner = arrayTesting;
            my_adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, arraySpinner);
            my_adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
            my_spinner.setAdapter(my_adapter);
        }
    }

    //  [networking] --> MyHttpHelper() --> callback_draw_spinner()
    private void draw_spinner()
    {
        Log.d("DM: draw_spinner", "... ");
        String string_ip = edittext_ip.getText().toString();
        String string_port = edittext_port.getText().toString();
        MyRestAPI my_api = new MyRestAPI(string_ip, string_port, my_context);
        if (my_api.isOnline())
        {
            new MyHttpHelper().execute( my_api.rest_get_full_url(), "get", "");
        }
        else
        {
            Toast.makeText(my_context,
                    "Houston, we have a networking problem",
                    Toast.LENGTH_SHORT).show();
        }
    }

    private void refresh_gui_after(String action)
    {
        Log.d("DM: refresh_gui_after", "... " + action);
        switch (action)
        {
            case "get":
                button2put.setVisibility(View.INVISIBLE);
                button2post.setVisibility(View.VISIBLE);
                button2delete.setVisibility(View.VISIBLE);
                break;
            case "put":
            case "post":
            case "delete":
            case "reset":
                draw_gui();
                break;
            default:
                button2put.setVisibility(View.VISIBLE);
                button2post.setVisibility(View.INVISIBLE);
                button2delete.setVisibility(View.INVISIBLE);
                break;
        }
    }

    private void action_for_button(Button button2click)
    {
        Log.d("DM: action_for_button", "... " + button2click.getText().toString());

        String resource_id = edittext_rid.getText().toString();
        String json_text = edittext_json.getText().toString();
        String result = "";

        switch (button2click.getId())
        {
            case R.id.button2put:
                result = wrapper_for_rest_utility(resource_id, json_text, "put");
                Toast.makeText(my_context, "putting " + resource_id + " then " + result,
                        Toast.LENGTH_SHORT).show();
                refresh_gui_after("put");
                break;
            case R.id.button2post:
                result = wrapper_for_rest_utility(resource_id, json_text, "post");
                Toast.makeText(my_context, "posting " + resource_id + " then " + result,
                        Toast.LENGTH_SHORT).show();
                refresh_gui_after("post");
                break;
            case R.id.button2delete:
                result = wrapper_for_rest_utility(resource_id, "", "delete");
                Toast.makeText(my_context, result,
                        Toast.LENGTH_SHORT).show();
                refresh_gui_after("delete");
                break;
            case R.id.button2reset:
                refresh_gui_after("reset");
                break;
            default: break;
        }
    }

    private void callback_draw_edittext(String string_text)
    {
        edittext_json.setText(string_text);
    }

    private void callback_toast(String message)
    {
        Toast.makeText(my_context, message,
                Toast.LENGTH_SHORT).show();
    }

    private void callback_draw_error_reason(String[] error)
    {

    }

    //  [networking] --> MyHttpHelper() --> callback_draw_edittext()
    private void action_for_spinner_selected(int position)
    {
        if (position > 0)
        {
            String resource_id = arraySpinner[position];
            Toast.makeText(my_context, "retrieving " + resource_id, Toast.LENGTH_SHORT).show();
            // retrieve json from rest API, show resource id and json content
            edittext_rid.setText(resource_id);
            // perform http request
            String string_ip = edittext_ip.getText().toString();
            String string_port = edittext_port.getText().toString();
            MyRestAPI my_api = new MyRestAPI(string_ip, string_port, my_context);
            if (my_api.isOnline())
            {
                new MyHttpHelper().execute(my_api.rest_get_full_url(resource_id), "get", "");
            }
            refresh_gui_after("get");
        }
        else
        {
            clean_gui();
        }
    }

    // trigger async http request; return roger that immediately for user friendly
    private String wrapper_for_rest_utility(String resource_id, String input_json, String action)
    {
        Log.d("DM: wrapper_for_rest...", "... " + resource_id);
        String data4return = "";
        String string_ip = edittext_ip.getText().toString();
        String string_port = edittext_port.getText().toString();
        MyRestAPI my_api = new MyRestAPI(string_ip, string_port, my_context);
        // perform http request
        if (my_api.isOnline())
        {
            String format = "to %s %s";
            data4return = String.format(format, action, resource_id);
            switch (action)
            {
                case "delete":
                    new MyHttpHelper().execute(my_api.rest_get_full_url(resource_id), action, "");
                    break;
                case "put":
                case "post":
                    new MyHttpHelper().execute(my_api.rest_get_full_url(resource_id),
                            action, input_json);
                    break;
                default:
                    Log.e("DM: wrapper_for_rest_", "fail to integrate " + action);
                    break;
            }
        }
        return data4return;
    }

    private void action_for_spinner_nothing_selected() {

    }

    // https://developer.android.com/training/basics/network-ops/connecting.html#connection
    class MyHttpHelper extends AsyncTask<String, Void, String>
    {
        String string_url = "";
        String string_method = "";
        String string_json = "";
        @Override
        protected String doInBackground(String... urls)  // --> returning value was stored in result of onPostExecute
        {
            string_url = urls[0];
            string_method = urls[1];
            string_json = urls[2];
            try
            {
                return doRest(string_url, string_method, string_json);
            } catch (IOException e) {
                return "Unable to retrieve web page. URL may be invalid.";
            }
        }
        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result)
        {
            Log.d("DM: onPostExecute", "to " + string_method + " " + string_url + " ... " + result);
            if (string_method.equals("delete"))
            {
                String[] returnedArray = parse_json_field_list(result);
                if (returnedArray.length == 2 && returnedArray[0].equals("string"))
                {
                    callback_toast(returnedArray[1] + " has been deleted");
                }
            }
            else if (string_method.equals("get"))
            {
                String[] returnedArray = parse_json_field_list(result);
                //for (String i:returnedArray) { Log.d("DM: onPostExecute", " --> " + i); }
                if (returnedArray.length >= 1)
                {
                    String decision = returnedArray[0];
                    switch (decision)
                    {
                        case "listing":
                            if (returnedArray.length > 1)
                            {
                                callback_draw_spinner(Arrays.copyOfRange(returnedArray, 1, returnedArray.length) );
                            }
                            else // empty
                            {
                                callback_draw_spinner(null);
                            }
                            break;
                        case "value":
                            callback_draw_edittext(returnedArray[1]);
                            break;
                        case "reason":
                            for (int i=1; i<returnedArray.length; i++)
                            {
                                Toast.makeText(my_context, "rest api: " + returnedArray[i],
                                        Toast.LENGTH_SHORT).show();
                            }
                            break;
                        default:
                            Log.e("onPostExecute", "Internal Programming Error: " + decision);
                            break;
                    }
                }
                else
                {
                    Log.e("onPostExecute", "Internal Programming Error");
                }
            }
            else // put. post, others
            {
                String[] returnedArray = parse_json_field_list(result);
                if (returnedArray.length > 0) // some error occurs,
                {
                    callback_draw_error_reason(returnedArray);
                }
            }
        }

        // http://stackoverflow.com/questions/309424/read-convert-an-inputstream-to-a-string
        private String convertStreamToString(java.io.InputStream is) {
            java.util.Scanner s = new java.util.Scanner(is).useDelimiter("\\A");
            return s.hasNext() ? s.next() : "";
        }

        // return String[]
        // String[0]: status code, N ~ 0 ~ -N
        // String[1 ~ n]:
        private String[] parse_json_field_list(String json_buffer)
        {
            String[] result = null;
            try {
                JSONObject object_json = new JSONObject(json_buffer);
                int status = object_json.getInt("status");
                Log.d("DM: parse_json_", "status = " + String.valueOf(status));
                Log.d("DM: parse_json_", "json_buffer = " + json_buffer);
                if (status > 0)  // listing (list) for element ids
                {
                    JSONArray array = object_json.getJSONArray("listing");
                    result = new String[array.length()+1];
                    for (int i = 0; i < array.length(); i++)
                    {
                        result[i+1] = array.getString(i);
                    }
                    result[0] = String.valueOf("listing");
                }
                else if (status == 0)  // value (string) , or listing ( empty list)
                {
                    if (object_json.has("value"))
                    {
                        try {
                            JSONObject inner = object_json.getJSONObject("value");
                            result = new String[2];
                            result[0] = String.valueOf("value");
                            result[1] = inner.toString(2);
                        }catch(JSONException e)
                        {
                            result = new String[2];
                            result[0] = String.valueOf("string");
                            result[1] = String.valueOf(object_json.getString("value"));
                        }
                    }
                    else if (object_json.has("listing"))
                    {
                        result = new String[1];
                        result[0] = String.valueOf("listing");
                    }
                }
                else // reason (list), for failure
                {
                    JSONArray array = object_json.getJSONArray("reason");
                    result = new String[array.length()+1];
                    for (int i = 0; i < array.length(); i++)
                    {
                        result[i+1] = array.getString(i);
                    }
                    result[0] = String.valueOf("reason");
                }

            }catch(JSONException e)
            {
                Log.w("DM: parse_json_", e.getMessage());
                result = new String[1];
                result[0] = String.valueOf(e.getMessage());
            }
            if (result == null)
            {
                result = new String[1];
                result[0] = String.valueOf("error");
            }
            return result;
        }

        // return String, which is http body
        private String doRest(String string_url, String string_method, String string_json) throws IOException
        {
            Log.d("DM: doRest", string_method + " " + string_url);
            InputStream is = null;
            int len = 1024; // http content length limitation
            try {
                URL url = new URL(string_url);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setReadTimeout(10000);
                conn.setConnectTimeout(15000);
                // http method
                conn.setRequestMethod(string_method.toUpperCase());
                // http body
                if (string_method.equals("put") || string_method.equals("post"))
                {
                    conn.setDoOutput(true);
                    conn.setRequestProperty("content-type", "application/json; charset=utf-8");
                    OutputStream os = conn.getOutputStream();
                    os.write(string_json.getBytes());
                    os.flush();
                    os.close();
                }
                conn.setDoInput(true);
                conn.connect();
                // response header
                int response = conn.getResponseCode();
                Log.d("DM: doRest", "HTTP code: " + response);
                // response body
                is = conn.getInputStream();
                String contentAsString = convertStreamToString(is);
                Log.d("DM: doRest", "HTTP body: " + contentAsString);
                return String.valueOf(contentAsString);
            } finally {
                if (is != null) {
                    try { is.close(); }
                    catch (IOException e) {
                        Log.w("DM: doRest", "fail to close input stream, " + e.getMessage());
                    }
                }
            }
        }
    }
}

class MyRestAPI
{
    private String string_ip = "";
    private String string_port = "";
    private String string_path = "/api/v1/resource";

    private Context my_context;

    public MyRestAPI(String ip, String port, Context context)
    {
        string_ip = ip;
        string_port = port;
        my_context = context;
    }

    public boolean isOnline()
    {
        ConnectivityManager connMgr = (ConnectivityManager)
                my_context.getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        return (networkInfo != null && networkInfo.isConnected());
    }

    protected String rest_get_full_url()
    {
        //String format = "http://%s:%s%s";
        //String string_returned = String.format(format, string_ip, string_port, string_path);
        //return string_returned;
        return rest_get_full_url("");
    }

    protected String rest_get_full_url(String string_id)
    {
        String string_returned;
        if (string_id.length() > 0)
        {
            String format = "http://%s:%s%s/%s";
            string_returned = String.format(format, string_ip, string_port, string_path, string_id);
        }
        else
        {
            String format = "http://%s:%s%s";
            string_returned = String.format(format, string_ip, string_port, string_path);
        }
        return string_returned;
    }

    protected String rest_get_option(String field_name)
    {
        return field_name;
    }

    protected String rest_put(String resource_id, String string_json)
    {
        //return "{\n" + " 'name': " + resource_id + ", \n" + " \n}";
        String str_format = "{\n  \'put\':%s,  \'data\':%s       \n}";
        return String.format(str_format, resource_id, string_json);
    }

    protected String rest_post(String resource_id, String string_json)
    {
        //return "{\n" + " 'name': " + resource_id + ", \n" + " \n}";
        String str_format = "{\n  \'post\':%s,  \'data\':%s       \n}";
        return String.format(str_format, resource_id, string_json);
    }


} // end of class MyRestAPI

