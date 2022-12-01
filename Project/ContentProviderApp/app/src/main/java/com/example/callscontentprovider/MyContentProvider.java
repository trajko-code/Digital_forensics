package com.example.callscontentprovider;

import android.content.ContentProvider;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Context;
import android.content.UriMatcher;
import android.database.Cursor;
import android.net.Uri;
import android.provider.CallLog;
import android.util.Log;

public class MyContentProvider extends ContentProvider {
    public MyContentProvider() {
    }

    static final String kTag = "MCP";

    // defining authority so that other application can access it
    static final String PROVIDER_NAME = "com.demo.user.provider";

    // defining content URI
    static final String URL = "content://" + PROVIDER_NAME + "/calls";

    // parsing the content URI
    static final Uri CONTENT_URI = Uri.parse(URL);

    static final int uriCallsCode = 1;
    static final UriMatcher uriMatcher;

    private ContentResolver myCr = null;

    static {
        // to match the content URI
        // every time user access table under content provider
        uriMatcher = new UriMatcher(UriMatcher.NO_MATCH);

        // to access whole table
        uriMatcher.addURI(PROVIDER_NAME, "calls", uriCallsCode);

        // to access a particular row
        // of the table
        //uriMatcher.addURI(PROVIDER_NAME, "users/*", uriCode);
    }

    @Override
    public String getType(Uri uri) {
        Log.i(kTag, "getType");
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @Override
    public boolean onCreate() {
        Log.i(kTag, "onCreate");
        Context context = getContext();
        myCr = context.getContentResolver();
        return true;
    }

    @Override
    public Cursor query(Uri uri, String[] projection, String selection,
                        String[] selectionArgs, String sortOrder) {
        Log.i(kTag, "query uri: " + uri.toString());

        if (myCr == null) {
            throw new UnsupportedOperationException("Content resolver didn't set");
        }

        Uri provider_uri = null;
        switch (uriMatcher.match(uri)) {
            case uriCallsCode:
                 provider_uri = CallLog.Calls.CONTENT_URI;
                 break;
            default:
                throw new IllegalArgumentException("Unknown URI " + uri);
        }

        return myCr.query(
                provider_uri,
                projection,
                selection,
                selectionArgs,
                sortOrder);
    }

    @Override
    public Uri insert(Uri uri, ContentValues values) {
        Log.i(kTag, "insert");
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @Override
    public int update(Uri uri, ContentValues values, String selection,
                      String[] selectionArgs) {
        Log.i(kTag, "update");
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @Override
    public int delete(Uri uri, String selection, String[] selectionArgs) {
        Log.i(kTag, "delete");
        throw new UnsupportedOperationException("Not yet implemented");
    }
}