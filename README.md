[![PyPI version](https://badge.fury.io/py/not.svg)](http://badge.fury.io/py/not)

### not
If anyone is interested in the halfway point between Geeknote & *a random collection of .txt files in $HOME*, meet me in the middle with 'not (note w/o the [e]vernote)', a low-friction, dumb as rocks, evernote based notekeeping thing.


### rationale
i need to take notes on a daily basis, but i hate all note taking software

i just want to scratch down some crap in vi and save it somewhere safe and synced

[Geeknote](http://www.geeknote.me/) is cool (and largely inspired not), but it's super feature rich and requires extra brain workyness that I don't often have.

`not` and I'm done

### install

for regular pip install:

`pip install not`

if you are cool, use [pex](https://github.com/pantsbuild/pex)!

`pex not -c not -o ~/bin/not && pex not -c not-setup -o ~/bin/not-setup`

then run the setup script:

`not-setup`


### usage
`not` -- creates or updates a note using your favorite editor, stored in default notebook, named after today's date

`not some_title` same thing, but instead of todays date it's whatever custom title you wrote

piping via stdin also works for ultimate lazyness:

`echo 'wow I am so lazy' | not`

to add tags, simply add a line to your note that starts with "tags:" and then a comma separated list
for example: `tags: these,are,tags`

don't remember the last couple notes you edited? just run

`not ls`

it will return a list of the last 10ish edited notes

* all notes are plaintext
* no notebook customization, just the default notebook
* line breaks and html aren't handled that well, sorry
* open to pull requests as long as the philosophy remains unchanged
