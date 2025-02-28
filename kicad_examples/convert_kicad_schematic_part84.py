# Warning: Large block split
<div id="LC65" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">            <span class=pl-s>&#39;space&#39;</span>,</div>
<div id="LC66" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">        ])</div>
<div id="LC67" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">
</div>
<div id="LC68" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">        <span class=pl-en>xdotool</span>([<span class=pl-s>&#39;key&#39;</span>, <span class=pl-s>&#39;Return&#39;</span>])</div>
<div id="LC69" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">
</div>
<div id="LC70" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">        <span class=pl-s1>time</span>.<span class=pl-c1>sleep</span>(<span class=pl-c1>2</span>)</div>
<div id="LC71" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">
</div>
<div id="LC72" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">        <span class=pl-s1>eeschema_proc</span>.<span class=pl-c1>terminate</span>()</div>
<div id="LC73" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">
</div>
<div id="LC74" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">    <span class=pl-c># print(exports_dir)</span></div>
<div id="LC75" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">
</div>
<div id="LC76" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-k>if</span> <span class=pl-s1>__name__</span> <span class=pl-c1>==</span> <span class=pl-s>&#39;__main__&#39;</span>:</div>
<div id="LC77" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">    <span class=pl-s1>desc</span> <span class=pl-c1>=</span> <span class=pl-s>&quot;&quot;&quot;</span></div>
<div id="LC78" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-s>    Converts a KiCAD schematic to SVG format for display and diff-ing.</span></div>
<div id="LC79" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-s>    A schematic can be provided as a file or as standard input.</span></div>
<div id="LC80" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-s>    The svg is written the supplied output directory.</span></div>
<div id="LC81" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-s>        &quot;&quot;&quot;</span></div>