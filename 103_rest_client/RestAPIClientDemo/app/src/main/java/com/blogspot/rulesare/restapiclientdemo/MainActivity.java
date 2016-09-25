package com.blogspot.rulesare.restapiclientdemo;

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
import java.security.SecureRandom;
import java.math.BigInteger;

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

    private void draw_spinner()
    {
        Log.d("DM: draw_spinner", "... ");
        // retrieve resource lists from REST API\
        String string_ip = edittext_ip.getText().toString();
        String string_port = edittext_port.getText().toString();
        MyRestAPI my_api = new MyRestAPI(string_ip,string_port);

        String[] returnedArray = my_api.rest_get();
        arrayTesting = new String[returnedArray.length];
        System.arraycopy(returnedArray, 0, arrayTesting,0, returnedArray.length);
        //for (int i=0; i<returnedArray.length; i++)
        //{
        //    arrayTesting[i] = returnedArray[i];
        //}
        arraySpinner = arrayTesting;
        my_adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, arraySpinner);
        my_adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        my_spinner.setAdapter(my_adapter);
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
                Toast.makeText(my_context, "deleting " + resource_id + " then " + result,
                        Toast.LENGTH_SHORT).show();
                refresh_gui_after("delete");
                break;
            case R.id.button2reset:
                refresh_gui_after("reset");
                break;
            default: break;
        }
    }

    private void action_for_spinner_selected(int position)
    {
        if (position > 0)
        {
            String resource_id = arraySpinner[position];
            Toast.makeText(my_context, "retrieving " + resource_id, Toast.LENGTH_SHORT).show();
            // retrieve json from rest API, show resource id and json content
            edittext_rid.setText(resource_id);
            edittext_json.setText(wrapper_for_rest_utility(resource_id, "", "get"));
            refresh_gui_after("get");
        }
        else
        {
            clean_gui();
        }
    }

    private String wrapper_for_rest_utility(
            String resource_id,
            String input_json,
            String action)
    {
        Log.d("DM: wrapper_for_rest...", "... " + resource_id);
        String data4return = "";
        MyRestAPI my_api = new MyRestAPI(edittext_ip.getText().toString(),
                edittext_port.getText().toString());
        switch(action)
        {
            case "get":
                if (resource_id.length()>0)
                {
                    data4return = my_api.rest_get(resource_id);
                }
                else
                {
                    data4return = "{\'status\'=\'internal error\'}";
                }
                break;
            case "put":
                data4return = my_api.rest_put(resource_id, input_json);
                break;
            case "post":
                data4return = my_api.rest_post(resource_id, input_json);
                break;
            case "delete":
                data4return = my_api.rest_delete(resource_id);
                break;
            default:
                data4return = "{\'status\'=\'out of scope\'}";
                break;
        }
        return data4return;
    }

    private void action_for_spinner_nothing_selected() {
        Toast.makeText(my_context,
                "[todo] nothing to do?",
                Toast.LENGTH_SHORT).show();
    }

}

class MyRestAPI
{
    private String string_ip = "";
    private String string_port = "";

    public MyRestAPI(String ip, String port)
    {
        string_ip = ip;
        string_port = port;
    }

    public String[] rest_get()
    {
        SecureRandom random = new SecureRandom();
        int number = random.nextInt(20);
        Log.d("DM: rest_get", "number = " + String.valueOf(number));
        String[] array = new String[number+1];
        array[0] = String.valueOf("... new create ...");
        for (int i=1; i< number+1; i++)
        {
            array[i] = new BigInteger(64, random).toString(40);
        }
        /*
        String[] array = new String[] {
                "... new create ...",
                "1111111111", "2222222222", "3333333333", "4444444444", "5555555555"
        };*/
        return array;
    }

    public String rest_get(String resource_id)
    {
        String str_format = "{\n  \'ip\':%s,  \'port\':%s       \n}";
        return String.format(str_format, string_ip, string_port);
    }

    public String rest_put(String resource_id, String string_json)
    {
        //return "{\n" + " 'name': " + resource_id + ", \n" + " \n}";
        String str_format = "{\n  \'put\':%s,  \'data\':%s       \n}";
        return String.format(str_format, resource_id, string_json);
    }

    public String rest_post(String resource_id, String string_json)
    {
        //return "{\n" + " 'name': " + resource_id + ", \n" + " \n}";
        String str_format = "{\n  \'post\':%s,  \'data\':%s       \n}";
        return String.format(str_format, resource_id, string_json);
    }

    public String rest_delete(String resource_id)
    {
        //return "{\n" + " 'name': " + resource_id + ", \n" + " \n}";
        String str_format = "{\n  \'delete\':%s,\n}";
        return String.format(str_format, resource_id);
    }

} // end of class MyRestAPI

