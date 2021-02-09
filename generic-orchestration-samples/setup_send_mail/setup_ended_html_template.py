from jinja2 import Template

HTML_TEMPLATE_STR = """
<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
  <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type" />
  <meta id="subject" content="Sandbox '{{ReservationName}}' has completed the setup stage at {{Now}} (UTC)"/>
  <title>Sandbox Setup Completed</title>
  <style type="text/css">
table {
background-color: #FFFFFF;
border: 1px solid #C3C3C3;
border-collapse: collapse;
font-size:9.0pt;
width:80%;
}
table th {
mso-style-priority:5;
mso-style-unhide:no;
mso-style-qformat:yes;
mso-style-locked:yes;
mso-style-link:"Subtitle Char";
margin:0cm;
margin-bottom:.0001pt;
mso-pagination:none;
font-size:9.0pt;
font-family:"Tw Cen MT","serif";
mso-ascii-font-family:"Tw Cen MT";
mso-ascii-theme-font:minor-latin;
mso-fareast-font-family:"Times New Roman";
mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:"Tw Cen MT";
mso-hansi-theme-font:minor-latin;
mso-bidi-font-family:Tahoma;
color: white;
text-transform:uppercase;
letter-spacing:.2pt;
font-weight:bold;
text-align: left;
border-style: solid; border-color: rgb(153, 153, 153) silver silver; border-width: 1pt 1pt 1pt; padding: 0.7pt 1.45pt 0.7pt 2.9pt; background: rgb(0,60,105) none repeat scroll 0%; -moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial; height: 18pt;
}
table td {
border: 1px solid #C3C3C3;
padding: 3px;
letter-spacing:.2pt;
font-size:9.0pt;
font-family:"Tw Cen MT","serif";
mso-ascii-font-family:"Tw Cen MT";
mso-ascii-theme-font:minor-latin;
mso-fareast-font-family:"Times New Roman";
mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:"Tw Cen MT";
mso-hansi-theme-font:minor-latin;
mso-bidi-font-family:Tahoma;
color: rgb(0,60,105);
}
h2
{mso-style-priority:1;
mso-style-unhide:no;
mso-style-qformat:yes;
mso-style-link:"Heading 2 Char";
margin:0cm;
margin-bottom:.0001pt;
mso-pagination:widow-orphan;
mso-outline-level:2;
font-size:12.0pt;
font-family:"Tw Cen MT","serif";
mso-ascii-font-family:"Tw Cen MT";
mso-ascii-theme-font:major-latin;
mso-fareast-font-family:"Times New Roman";
mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:"Tw Cen MT";
mso-hansi-theme-font:major-latin;
mso-bidi-font-family:Tahoma;
letter-spacing:.2pt;
font-weight:normal;}
h3
{mso-style-priority:1;
mso-style-unhide:no;
mso-style-qformat:yes;
mso-style-link:"Heading 3 Char";
margin:0cm;
margin-bottom:.0001pt;
mso-pagination:widow-orphan;
mso-outline-level:3;
font-size:15.0pt;
font-family:"Tw Cen MT","serif";
mso-ascii-font-family:"Tw Cen MT";
mso-ascii-theme-font:major-latin;
mso-fareast-font-family:"Times New Roman";
mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:"Tw Cen MT";
mso-hansi-theme-font:major-latin;
mso-bidi-font-family:Tahoma;
color:rgb(0,60,105);
text-transform:uppercase;
letter-spacing:.2pt;
font-weight:normal;}
h4
{mso-style-priority:1;
mso-style-unhide:no;
mso-style-qformat:yes;
mso-style-link:"Heading 3 Char";
margin:0cm;
margin-bottom:.0001pt;
mso-pagination:widow-orphan;
mso-outline-level:3;
font-size:15.0pt;
font-family:"Tw Cen MT","serif";
mso-ascii-font-family:"Tw Cen MT";
mso-ascii-theme-font:major-latin;
mso-fareast-font-family:"Times New Roman";
mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:"Tw Cen MT";
mso-hansi-theme-font:major-latin;
mso-bidi-font-family:Tahoma;
color:#7F3A95;
font-style: italic;
letter-spacing:.2pt;
font-weight:normal;}
body
{
	color: rgb(0,60,105);
}
  </style>
</head>
<body>
<h4>CloudShell Sandbox Notification</h4>
<br/>
<h3>{{ReservationName}}</h3>
<h2>Sandbox '{{ReservationName}}' has completed the setup stage at {{Now}} (UTC), and is ready for use</h2>
<a href="{{ReservationLink}}">{{ReservationLink}}</a><br/><br/>
<table border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
        <th style="width: 110pt;">OWNER</th>
        <td>{{ReservationOwner}}</td>
    </tr>
    <tr>
      <th style="width: 110pt;">ID</th>
      <td>{{ReservationId}}</td>
    </tr>
    <tr>
      <th style="width: 110pt;">START TIME</th>
      <td>{{ReservationStartTime}} (UTC)</td>
    </tr>
    <tr>
      <th style="width: 110pt;">PLANNED END TIME</th>
      <td>{{ReservationEndTime}} (UTC)</td>
    </tr>
    <tr>
      <th style="width: 110pt;">DESCRIPTION</th>
      <td><pre>{{ReservationDescription}}</pre></td>
    </tr>
    <tr>
      <th style="width: 110pt;">NUMBER OF RESOURCES</th>
      <td>{{ReservationNumberOfResources}}</td>
    </tr>
    <tr>
      <th style="width: 110pt;">MAIN BLUEPRINT</th>
      <td>{{ReservationMainTopology}}</td>
    </tr>
  </tbody>
</table>
</body>
</html>
"""


def get_email_template(sb_name, res_id, current_time, training_portal_link, sb_owner, start_time, end_time,
                       sb_description, resource_count, blueprint_name):
    jinja_template = Template(HTML_TEMPLATE_STR)
    return jinja_template.render(ReservationName=sb_name,
                                 Now=current_time,
                                 ReservationLink=training_portal_link,
                                 ReservationOwner=sb_owner,
                                 ReservationId=res_id,
                                 ReservationStartTime=start_time,
                                 ReservationEndTime=end_time,
                                 ReservationDescription=sb_description,
                                 ReservationNumberOfResources=resource_count,
                                 ReservationMainTopology=blueprint_name)


if __name__ == "__main__":
    x = get_email_template(sb_name="my sandbox",
                           res_id="xxxxxDDDDDaaaaa",
                           current_time="lol o'clock",
                           training_portal_link="my link to portal",
                           sb_owner="natti",
                           start_time="now",
                           end_time="later",
                           sb_description="whatevs",
                           resource_count="9",
                           blueprint_name="my bp")
    pass






















