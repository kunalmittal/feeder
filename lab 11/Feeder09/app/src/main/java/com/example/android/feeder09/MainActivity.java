package com.example.android.feeder09;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

import static android.icu.lang.UCharacter.GraphemeClusterBreak.T;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView welcome_name_textView = (TextView) findViewById(R.id.welcome_name);
        Intent intent = getIntent();
        String main_name = intent.getStringExtra("name_main");
        welcome_name_textView.setText(main_name);
    }
}
