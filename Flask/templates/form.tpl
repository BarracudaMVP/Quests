<form action = '/add' method=POST>
<input type=hidden name=id value={{id}}>
Title:<input type=text name=title value={{title}}><br>
Author:<input type=text name=author value={{author}}>
<br><textarea name=body rows=10 cols=30 wrap=virtual>{{body}}</textarea>
<br><input type=submit value="Ok">
</form>
