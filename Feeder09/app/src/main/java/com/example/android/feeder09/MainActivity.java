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

import java.util.ArrayList;

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





        String json_text = sharedPreferences.getString("json_text","");
        try{
            JSONObject obj = new JSONObject(json_text);
            JSONArray myArray = (JSONArray) obj.get("courses");

            ArrayList<CalendarDay> redDates = new ArrayList<>();
            ArrayList<CalendarDay> blueDates = new ArrayList<>();

            for(int i=0;i<myArray.length();i++){
                JSONObject currObj = (JSONObject) myArray.get(i);
                String course_number =(String) currObj.get("course_number");
                JSONArray courseFeedbacks = (JSONArray) currObj.get("feedback_forms");
                JSONArray assignments = (JSONArray) currObj.get("assignment_deadline");

                for(int j=0;j<courseFeedbacks.length();j++){
                    JSONObject currFeedback = (JSONObject) courseFeedbacks.get(j);
                    String fdate = (String) currFeedback.get("feedback_deadline_datetime");

                    String fname = (String) currFeedback.get("feedback_name");
                    JSONArray fques = (JSONArray) currFeedback.get("feedback_questions");

                    String[] date =fdate.split(" ")[0].split("-");
                    CalendarDay calendarDay = CalendarDay.from(Integer.parseInt(date[0]),Integer.parseInt(date[1]),Integer.parseInt(date[2]));
                    redDates.add(calendarDay);
                }

                for(int k=0;k<assignments.length();k++){
                    JSONObject currassignment = (JSONObject) assignments.get(k);

                    String dname = (String) currassignment.get("deadline_name");
                    String ddate = (String) currassignment.get("deadline_datetime");

                    String[] date =ddate.split(" ")[0].split("-");
                    CalendarDay calendarDay = CalendarDay.from(Integer.parseInt(date[0]),Integer.parseInt(date[1]),Integer.parseInt(date[2]));
                    blueDates.add(calendarDay);
                }

            }

            calendarView.addDecorator(
                    new EventDecorator(Color.RED, redDates)
            );
            calendarView.addDecorator(
                    new EventDecorator(Color.BLUE, blueDates)
            );
        }catch (JSONException e){}

    }


    public class CustomCalendarListener implements OnDateSelectedListener {
        @Override
        public void onDateSelected(MaterialCalendarView calendarView, CalendarDay date, boolean selected) {

        }
    };
}





