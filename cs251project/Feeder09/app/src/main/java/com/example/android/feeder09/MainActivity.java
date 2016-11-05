package com.example.android.feeder09;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.prolificinteractive.materialcalendarview.CalendarDay;
import com.prolificinteractive.materialcalendarview.MaterialCalendarView;
import com.prolificinteractive.materialcalendarview.OnDateSelectedListener;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import static android.icu.lang.UCharacter.GraphemeClusterBreak.T;
import static com.example.android.feeder09.R.id.logout_button;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        SharedPreferences sharedPreferences = getSharedPreferences("MyPreferences", Context.MODE_PRIVATE);
        boolean isLoggedIn = sharedPreferences.getBoolean("isLoggedIn",false);  //false is the value when key doesn't exist
        if(!isLoggedIn){
            Intent intent = new Intent(this, LoginActivity.class);
            startActivity(intent);
        }



        setContentView(R.layout.activity_main);

        TextView welcome_name_textView = (TextView) findViewById(R.id.welcome_name);
        String main_name = sharedPreferences.getString("username","");
        welcome_name_textView.setText("Welcome "+main_name);

        Button logout_button  = (Button) findViewById(R.id.logout_button);
        logout_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                SharedPreferences sharedPreferences = getSharedPreferences("MyPreferences", Context.MODE_PRIVATE);
                SharedPreferences.Editor editor = sharedPreferences.edit();
                editor.putBoolean("isLoggedIn", false);
                editor.putString("username", "");
                editor.commit();

                Intent intent = new Intent(getApplicationContext(), LoginActivity.class);
                startActivity(intent);
            }

        });

        MaterialCalendarView calendarView = (MaterialCalendarView) findViewById(R.id.calendarView);
        calendarView.setOnDateChangedListener(new CustomCalendarListener());
//        calendarView.addDecorator(
//                new EventDecorator(Color.RED, red_dates)
//        );
        String json_text = sharedPreferences.getString("json_text","");
        try{
            JSONArray myArray = new JSONArray(json_text);
            System.out.println(json_text);
            for(int i=0;i<myArray.length();i++){
                JSONObject currobj = (JSONObject) myArray.get(i);
                JSONObject allFields = (JSONObject) currobj.get("fields");
                String course_num = (String) allFields.get("course_number");
                System.out.println(course_num);
            }
        }catch (JSONException e){}

    }


    public class CustomCalendarListener implements OnDateSelectedListener {
        @Override
        public void onDateSelected(MaterialCalendarView calendarView, CalendarDay date, boolean selected) {

        }
    };
}





