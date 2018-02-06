# Barnamak

- **Category :** reverse
- **Points :** 200
- **Description :**
```
Run the application and capture the flag!
```

# Writeup
The application is an Android apk file, so we can easily decompile it. We used http://www.javadecompilers.com/apk for this job. Just in case we miss anything we also decompiled the apk using apktool.
At first glance the apk doesn't seem to have a lot of code, and no native libraries which is a good sign and will make our work easier. The first things to look for are obvious encryption attempts such as unusual strings, or raw byte arrays. In the file ChallengeFragment.java we stumble upon three pretty promising function :

```java
    class C02611 implements OnClickListener {
        C02611() {
        }

        public void onClick(DialogInterface context, int which) {
            if (C0259c.m5a() || C0259c.m6b() || C0259c.m7c()) {
                int[] aa1 = new int[]{147, 146, 71, 53, 172, 150, 128, 117, 124, 141, 164, 118, 173, 163, 172, 139, 159, 173, 166, 114, 125, 137, 60, 112, 135, 136, 152, 112, 172, 153, 136, TransportMediator.KEYCODE_MEDIA_PAUSE, 151, 172, 175, 79, 134, 136, 75, 116, 135, 115, 135, TransportMediator.KEYCODE_MEDIA_RECORD, 125, 55, 147, 116, 157, 55, 168, TransportMediator.KEYCODE_MEDIA_PLAY, 134, 76, 158, 52, 124, 163, 125, 75, 173, 164, 67, 57};
                String Res = ChallengeFragment.iia(new int[]{162, 136, 133, 131, 68, 141, 119, 68, 169, 160, 49, 68, 171, TransportMediator.KEYCODE_MEDIA_RECORD, 68, 168, 139, 138, 131, 112, 141, 113, 128, 129}, String.valueOf((int) Math.round(ChallengeFragment.this.location.getLatitude())));
                Toast.makeText(ChallengeFragment.this.getActivity().getBaseContext(), Res, 0).show();
                ChallengeFragment.this.textViewLatitude1 = (TextView) ChallengeFragment.this.view.findViewById(C0257R.id.TextView_C);
                ChallengeFragment.this.textViewLatitude1.setText(Res);
                System.exit(0);
            }
        }
    }

 
```

```java
   public boolean m11b() {
        Integer i = Integer.valueOf(Integer.parseInt("2C", 16));
        int aat = i.intValue() + 1;
        int bbt = (-Integer.valueOf(Integer.parseInt("5B", 16)).intValue()) - 2;
        if (this.location == null) {
            return false;
        }
        if (((int) this.location.getLatitude()) == aat && ((int) this.location.getLongitude()) == bbt) {
            ((Vibrator) this.context.getSystemService("vibrator")).hasVibrator();
            Toast.makeText(this.context, getString(C0257R.string.string_a), 0).show();
            return true;
        }
        Toast.makeText(this.context, getString(C0257R.string.string_b), 0).show();
        return false;
    }


```

```java
  private static String iia(int[] input, String key) {
        String output = "";
        for (int i = 0; i < input.length; i++) {
            output = output + ((char) ((input[i] - 48) ^ key.charAt(i % (key.length() - 1))));
        }
        return output;
    }


```

The first one seems to decrypt an array using the third function, and using as a key the current device latitude (casted to int then string). Interestingly the second function seems to do comparisons on latitude and longitude. To make the second function return true we need to have a latitude of 0x2C + 0x1 = 45 and a longitude of -0x5b - 0x2 = -93. Now that we have what we suppose are the correct locations we can decrypt the array in the first function using our latitude (43).
We get the string : "Flag is MD5 Of Longtiude"
Our key is an int converted to string, so we just have to do : 
```
$ echo -ne "-93" | md5sum
87a20a335768a82441478f655afd95fe  -
```

And the flag is : **SharifCTF{87a20a335768a82441478f655afd95fe}**
