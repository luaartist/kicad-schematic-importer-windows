# Warning: Large block split
<div id="LC2" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-c>#   Licensed under the Apache License, Version 2.0 (the &quot;License&quot;);</span></div>
<div id="LC3" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-c>#   you may not use this file except in compliance with the License.</span></div>
<div id="LC4" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-c>#   You may obtain a copy of the License at</span></div>
<div id="LC5" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-c>#</span></div>
<div id="LC6" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-c>#       http://www.apache.org/licenses/LICENSE-2.0</span></div>
<div id="LC7" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-c>#</span></div>
<div id="LC8" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-c>#   Unless required by applicable law or agreed to in writing, software</span></div>
<div id="LC9" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-c>#   distributed under the License is distributed on an &quot;AS IS&quot; BASIS,</span></div>
<div id="LC10" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-c>#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.</span></div>
<div id="LC11" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-c>#   See the License for the specific language governing permissions and</span></div>
<div id="LC12" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-c>#   limitations under the License.</span></div>
<div id="LC13" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-k>import</span> <span class=pl-s1>os</span></div>
<div id="LC14" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-k>import</span> <span class=pl-s1>sys</span></div>
<div id="LC15" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-k>import</span> <span class=pl-s1>time</span></div>
<div id="LC16" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-k>import</span> <span class=pl-s1>argparse</span></div>
<div id="LC17" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">
</div>
<div id="LC18" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-c># Get the path of this script</span></div>