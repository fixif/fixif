function varargout = wdf_GUI(varargin)
%WDF_GUI M-file for wdf_GUI.fig
%      WDF_GUI, by itself, creates a new WDF_GUI or raises the existing
%      singleton*.
%
%      H = WDF_GUI returns the handle to a new WDF_GUI or the handle to
%      the existing singleton*.
%
%      WDF_GUI('Property','Value',...) creates a new WDF_GUI using the
%      given property value pairs. Unrecognized properties are passed via
%      varargin to wdf_GUI_OpeningFcn.  This calling syntax produces a
%      warning when there is an existing singleton*.
%
%      WDF_GUI('CALLBACK') and WDF_GUI('CALLBACK',hObject,...) call the
%      local function named CALLBACK in WDF_GUI.M with the given input
%      arguments.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help wdf_GUI

% Last Modified by GUIDE v2.5 17-Oct-2005 12:17:40

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @wdf_GUI_OpeningFcn, ...
                   'gui_OutputFcn',  @wdf_GUI_OutputFcn, ...
                   'gui_LayoutFcn',  [], ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
   gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before wdf_GUI is made visible.
function wdf_GUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to wdf_GUI (see VARARGIN)

% Choose default command line output for wdf_GUI
handles.output = hObject;

% Update handles structure
handles.approxMethod       = 'butter';
set( handles.radiobutton_Butter, 'Value', 1 );
set( handles.edit_passBandRipple_dB,    'Visible', 'off' );
set( handles.edit_stopBandRipple_dB,    'Visible', 'off' );
set( handles.edit_stopBandZeros,        'Visible', 'off' );
set( handles.edit_stopBandZerosVector,  'Visible', 'off' );
set( handles.edit_nUnitElements,        'Visible', 'off' );
set( handles.edit_unitElementsVector,   'Visible', 'off' );
set( handles.popupmenu_SkwirzynskiType, 'Visible', 'off' );
set( handles.radiobutton_freqModeS,     'Visible', 'off' );
handles.filterOrder         =   [];
handles.cutOffFrequency     =  1.0;
set( handles.edit_cutOffFrequency,    'String', '1.0' );
handles.passBandRipple_dB   =   [];
handles.stopBandRipple_dB   =   [];
handles.skwirMode           =  'A';
checkbox_keepRatio          =    0;
set( handles.checkbox_keepRatio,      'Value', 0 );
set( handles.checkbox_keepRatio,        'Visible', 'off' );
handles.stopBandZeros       =   [];
handles.stopBandZerosVector =   [];
handles.nUnitElements       =    0;
handles.unitElementsVector  =   [];
handles.freqNormMode        =    1;
set( handles.radiobutton_freqMode1,   'Value', 1 );
handles.sDomain             =    1;
set( handles.radiobutton_sDomain,     'Value', 1 );
handles.filterType          = 'lp';
set( handles.radiobutton_LowPass,     'Value', 1 );
handles.centerFrequency     =   [];
handles.bandWidth           =   [];
set( handles.edit_centerFrequency,    'Visible', 'off' );
set( handles.edit_bandWidth,          'Visible', 'off' );
set( handles.radiobutton_serialFirst, 'Value', 1 );
set( handles.radiobutton_serialFirst, 'Visible', 'off');
set( handles.radiobutton_shuntFirst,  'Visible', 'off');
set( handles.checkbox_use2ports,      'Visible', 'off');
set( handles.checkbox_useSym,         'Visible', 'off');
handles.figHsShown         =     0;
handles.figHzShown         =     0;
handles.figsLadderShown    =     0;
handles.figsWDFShown       =     0;
handles.figsLWDFShown      =     0;
guidata( hObject, handles );

% use a .png file for the logo with a transparant background ...
TUD_logo = 'TUD_bl-zw.png';
set(hObject, 'Units', 'pixels' );
% ... and let this machine's set-up fill in the background
handles.logo1 = imread( TUD_logo,'BackgroundColor', get(hObject,'Color') );
axes(handles.axes2);
image(handles.logo1);
set(handles.axes2, 'Visible', 'off', 'Units', 'pixels' );

% UIWAIT makes wdf_GUI wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = wdf_GUI_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


function radiobutton_Butter_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_Butter, 'Value' ) == 0 )
		set( handles.radiobutton_Butter,  'Value', 1 );
	else
		off = [ handles.radiobutton_Cheby, handles.radiobutton_InvCheby, ...
				handles.radiobutton_Cauer, handles.radiobutton_Vlach ];
		lfMutualExclude( off );
		handles.approxMethod = 'butter';
		if ( handles.filterOrder == 0 )
			handles.filterOrder = [];
			set( handles.edit_filterOrder, 'String', '' );
		end			
		set( handles.edit_passBandRipple_dB,    'Visible', 'off' );
		set( handles.edit_stopBandRipple_dB,    'Visible', 'off' );
		set( handles.edit_stopBandZeros,        'Visible', 'off' );
		set( handles.checkbox_keepRatio,        'Visible', 'off'  );
		set( handles.edit_stopBandZerosVector,  'Visible', 'off' );
		set( handles.edit_nUnitElements,        'Visible', 'off' );
		set( handles.edit_unitElementsVector,   'Visible', 'off' );
		set( handles.popupmenu_SkwirzynskiType, 'Visible', 'off' );
		set( handles.radiobutton_freqModeS,     'Visible', 'off' );
		if ( handles.freqNormMode == -1 )
			handles.freqNormMode = 1;
			set( handles.radiobutton_freqMode1, 'Value', 1 );
			set( handles.radiobutton_freqModeS, 'Value', 0 );
		end
	end
	guidata( hObject, handles );			% store the changes

				
function radiobutton_Cheby_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_Cheby, 'Value' ) == 0 )
		set( handles.radiobutton_Cheby,  'Value', 1 );
	else
		off = [ handles.radiobutton_Butter, handles.radiobutton_InvCheby, ...
				handles.radiobutton_Cauer, handles.radiobutton_Vlach ];
		lfMutualExclude( off );
		handles.approxMethod = 'cheby';
		if ( handles.filterOrder == 0 )
			handles.filterOrder = [];
			set( handles.edit_filterOrder, 'String', '' );
		end			
		set( handles.edit_passBandRipple_dB,    'Visible', 'on'  );
		set( handles.edit_stopBandRipple_dB,    'Visible', 'off' );
		set( handles.edit_stopBandZeros,        'Visible', 'off' );
		set( handles.checkbox_keepRatio,        'Visible', 'off'  );
		set( handles.edit_stopBandZerosVector,  'Visible', 'off' );
		set( handles.edit_nUnitElements,        'Visible', 'off' );
		set( handles.edit_unitElementsVector,   'Visible', 'off' );
		set( handles.popupmenu_SkwirzynskiType, 'Visible', 'off' );
		set( handles.radiobutton_freqModeS,     'Visible', 'off' );
		if ( handles.freqNormMode == -1 )
			handles.freqNormMode = 1;
			set( handles.radiobutton_freqMode1, 'Value', 1 );
			set( handles.radiobutton_freqModeS, 'Value', 0 );
		end
	end
	guidata( hObject, handles );			% store the changes


function radiobutton_InvCheby_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_InvCheby, 'Value' ) == 0 )
		set( handles.radiobutton_InvCheby,  'Value', 1 );
	else
		off = [ handles.radiobutton_Butter, handles.radiobutton_Cheby, ...
				handles.radiobutton_Cauer, handles.radiobutton_Vlach ];
		lfMutualExclude( off );
		handles.approxMethod = 'invcheby';
		if ( handles.filterOrder == 0 )
			handles.filterOrder = [];
			set( handles.edit_filterOrder, 'String', '' );
		end			
		set( handles.edit_passBandRipple_dB,    'Visible', 'off' );
		set( handles.edit_stopBandRipple_dB,    'Visible', 'on'  );
		set( handles.edit_stopBandZeros,        'Visible', 'off' );
		set( handles.checkbox_keepRatio,        'Visible', 'off'  );
		set( handles.edit_stopBandZerosVector,  'Visible', 'off' );
		set( handles.edit_nUnitElements,        'Visible', 'off' );
		set( handles.edit_unitElementsVector,   'Visible', 'off' );
		set( handles.popupmenu_SkwirzynskiType, 'Visible', 'off' );
		set( handles.radiobutton_freqModeS,     'Visible', 'off' );
		if ( handles.freqNormMode == -1 )
			handles.freqNormMode = 1;
			set( handles.radiobutton_freqMode1, 'Value', 1 );
			set( handles.radiobutton_freqModeS, 'Value', 0 );
		end
	end
	guidata( hObject, handles );			% store the changes


function radiobutton_Cauer_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_Cauer, 'Value' ) == 0 )
		set( handles.radiobutton_Cauer,  'Value', 1 );
	else
		off = [ handles.radiobutton_Butter, handles.radiobutton_Cheby, ...
				handles.radiobutton_InvCheby, handles.radiobutton_Vlach ];
		lfMutualExclude( off );
		handles.approxMethod = 'cauer';
		if ( handles.filterOrder == 0 )
			handles.filterOrder = [];
			set( handles.edit_filterOrder, 'String', '' );
		end			
		set( handles.edit_passBandRipple_dB,    'Visible', 'on'  );
		set( handles.edit_stopBandRipple_dB,    'Visible', 'on'  );
		set( handles.edit_stopBandZeros,        'Visible', 'off' );
		set( handles.checkbox_keepRatio,        'Visible', 'off'  );
		set( handles.edit_stopBandZerosVector,  'Visible', 'off' );
		set( handles.edit_nUnitElements,        'Visible', 'off' );
		set( handles.edit_unitElementsVector,   'Visible', 'off' );
		set( handles.popupmenu_SkwirzynskiType, 'Visible', 'on'  );
		set( handles.radiobutton_freqModeS,     'Visible', 'on'  );
	end
	guidata( hObject, handles );			% store the changes


% --- Executes during object creation, after setting all properties.
function popupmenu_SkwirzynskiType_CreateFcn(hObject, eventdata, handles)
	if ispc
    	set( hObject, 'BackgroundColor','white');
	else
    	set( hObject, 'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
	end

% --- Executes on selection change in popupmenu_SkwirzynskiType.
function popupmenu_SkwirzynskiType_Callback(hObject, eventdata, handles)
	contents = get( hObject, 'String');
	handles.skwirMode = contents{ get( hObject, 'Value' ) };
	guidata( hObject, handles );			% store the changes


function radiobutton_Vlach_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_Vlach, 'Value' ) == 0 )
		set( handles.radiobutton_Vlach,  'Value', 1 );
	else
		off = [ handles.radiobutton_Butter, handles.radiobutton_Cheby, ...
				handles.radiobutton_InvCheby, handles.radiobutton_Cauer ];
		lfMutualExclude( off );
		handles.approxMethod = 'vlach';
		set( handles.edit_passBandRipple_dB,    'Visible', 'on'  );
		set( handles.edit_stopBandRipple_dB,    'Visible', 'off' );
		set( handles.edit_stopBandZeros,        'Visible', 'on'  );
		set( handles.checkbox_keepRatio,        'Visible', 'on'  );
		set( handles.edit_nUnitElements,        'Visible', 'on'  );
		set( handles.popupmenu_SkwirzynskiType, 'Visible', 'off' );
		set( handles.radiobutton_freqModeS,     'Visible', 'off' );
		if ( handles.freqNormMode == -1 )
			handles.freqNormMode = 1;
			set( handles.radiobutton_freqMode1, 'Value', 1 );
			set( handles.radiobutton_freqModeS, 'Value', 0 );
		end
		nStopBandZeros = length( handles.stopBandZeros );
		nPossibleStopBandZeros = floor( handles.filterOrder / 2 );
		handles.stopBandZerosVector = [ ones(1,nStopBandZeros) ...
									zeros(1,nPossibleStopBandZeros-nStopBandZeros) ];
		infoStr = num2str( handles.stopBandZerosVector );
		set( handles.edit_stopBandZerosVector, 'String', infoStr );										
		if ( get( handles.checkbox_ladderNetwork, 'Value' ) == 1 )
			set( handles.edit_stopBandZerosVector,  'Visible', 'on'  );
			set( handles.edit_unitElementsVector,   'Visible', 'on'  );
		end
	end
	guidata( hObject, handles );			% store the changes


% --- Executes during object creation, after setting all properties.
function edit_filterOrder_CreateFcn(hObject, eventdata, handles)
	% Hint: edit controls usually have a white background on Windows.
	%       See ISPC and COMPUTER.
	if ispc
    	set( hObject, 'BackgroundColor','white');
	else
    	set( hObject, 'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
	end

function edit_filterOrder_Callback(hObject, eventdata, handles)
	prevValue = handles.filterOrder;
	filterOrder = round( str2double( get( hObject, 'String' ) ) );
	if ( filterOrder >= 0 )
		if strcmp( handles.approxMethod, 'vlach' )
			nStopBandZeros = length( handles.stopBandZeros );
			nPossibleStopBandZeros = floor( filterOrder / 2 );
			if ( nStopBandZeros > nPossibleStopBandZeros )
				errordlg( 'Too many stopband zeros for this filterorder ...', ...
									'FilterOrder vs stopBandZeros mismatch', 'modal' );
				valid = 0;
			else
				handles.stopBandZerosVector = [ ones(1,nStopBandZeros) ...
										zeros(1,nPossibleStopBandZeros-nStopBandZeros) ];
				infoStr = num2str( handles.stopBandZerosVector );
				set( handles.edit_stopBandZerosVector, 'String', infoStr );										
				valid = 1;
			end
		else
			valid = ( filterOrder > 0 );
		end
	else
		valid = 0;
	end
	if ~valid
		beep;
		filterOrder = prevValue;
	end
	handles.filterOrder = filterOrder;
	guidata( hObject, handles );			% store the changes
	set( hObject, 'String', int2str(filterOrder) );


% --- Executes during object creation, after setting all properties.
function edit_passBandRipple_dB_CreateFcn(hObject, eventdata, handles)
	if ispc
    	set( hObject, 'BackgroundColor','white');
	else
    	set( hObject, 'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
	end

function edit_passBandRipple_dB_Callback(hObject, eventdata, handles)
	% use str2NUM here, to enable an empty string in case of a bireciprocal cauer design 
	handles.passBandRipple_dB = abs( str2num(get( hObject, 'String')) );
	set( hObject, 'String', num2str(handles.passBandRipple_dB) );
	guidata( hObject, handles );			% store the changes



% --- Executes during object creation, after setting all properties.
function edit_stopBandRipple_dB_CreateFcn(hObject, eventdata, handles)
	if ispc
    	set( hObject, 'BackgroundColor','white');
	else
    	set( hObject, 'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
	end

function edit_stopBandRipple_dB_Callback(hObject, eventdata, handles)
	handles.stopBandRipple_dB = abs( str2double(get( hObject, 'String')) );
	guidata( hObject, handles );			% store the changes



function radiobutton_freqMode1_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_freqMode1, 'Value' ) == 0 )
		set( handles.radiobutton_freqMode1, 'Value', 1 );
	else
		off = [ handles.radiobutton_freqMode0, handles.radiobutton_freqModeS ];
		lfMutualExclude( off );
		handles.freqNormMode = 1;
	end
	guidata( hObject, handles );			% store the changes


function radiobutton_freqMode0_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_freqMode0, 'Value' ) == 0 )
		set( handles.radiobutton_freqMode0, 'Value', 1 );
	else
		off = [ handles.radiobutton_freqMode1, handles.radiobutton_freqModeS ];
		lfMutualExclude( off );
		handles.freqNormMode = 0;
	end
	guidata( hObject, handles );			% store the changes


function radiobutton_freqModeS_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_freqModeS, 'Value' ) == 0 )
		set( handles.radiobutton_freqModeS, 'Value', 1 );
	else
		off = [ handles.radiobutton_freqMode0, handles.radiobutton_freqMode1 ];
		lfMutualExclude( off );
		handles.freqNormMode = -1;
	end
	guidata( hObject, handles );			% store the changes



function radiobutton_sDomain_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_sDomain, 'Value' ) == 0 )
		set( handles.radiobutton_sDomain, 'Value', 1 );
	else
		set( handles.radiobutton_zDomain, 'Value', 0 );
		handles.sDomain = 1;
		%---
		handles.cutOffFrequency = lfSwitchDomain( handles.cutOffFrequency, 's' );
		set( handles.edit_cutOffFrequency, 'String', ...
											lfFormattedString(handles.cutOffFrequency) );
		%---
		handles.stopBandZeros   = lfSwitchDomain( handles.stopBandZeros, 's' );
		set( handles.edit_stopBandZeros, 'String', ...
											lfFormattedString(handles.stopBandZeros) );
		%---
		if ~isempty( handles.centerFrequency )
			handles.centerFrequency = lfSwitchDomain( handles.centerFrequency, 's' );
			set( handles.edit_centerFrequency, 'String', ...
											lfFormattedString(handles.centerFrequency) );
		end
		%---
		if ~isempty( handles.bandWidth )
			handles.bandWidth = lfSwitchDomain( handles.bandWidth, 's' );
			set( handles.edit_bandWidth, 'String', lfFormattedString(handles.bandWidth) );
		end
	end
	guidata( hObject, handles );			% store the changes


function radiobutton_zDomain_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_zDomain, 'Value' ) == 0 )
		set( handles.radiobutton_zDomain, 'Value', 1 );
	else
		set( handles.radiobutton_sDomain, 'Value', 0 );
		handles.sDomain = 0;
		%---
		handles.cutOffFrequency = lfSwitchDomain( handles.cutOffFrequency, 'z' );
		set( handles.edit_cutOffFrequency, 'String', ...
											lfFormattedString(handles.cutOffFrequency) );
		%---
		handles.stopBandZeros   = lfSwitchDomain( handles.stopBandZeros, 'z' );
		set( handles.edit_stopBandZeros, 'String', ...
											lfFormattedString(handles.stopBandZeros) );
		%---
		if ~isempty( handles.centerFrequency )
			handles.centerFrequency = lfSwitchDomain( handles.centerFrequency, 'z' );
			set( handles.edit_centerFrequency, 'String', ...
											lfFormattedString(handles.centerFrequency) );
		end
		%---
		if ~isempty( handles.bandWidth )
			handles.bandWidth = lfSwitchDomain( handles.bandWidth, 'z' );
			set( handles.edit_bandWidth, 'String', lfFormattedString(handles.bandWidth) );
		end
	end
	guidata( hObject, handles );			% store the changes



% --- Executes during object creation, after setting all properties.
function edit_cutOffFrequency_CreateFcn(hObject, eventdata, handles)
	if ispc
    	set( hObject, 'BackgroundColor','white');
	else
    	set( hObject, 'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
	end


function edit_cutOffFrequency_Callback(hObject, eventdata, handles)
	newValue = str2double(get( hObject, 'String'));
	if ( ( handles.sDomain == 0 )  & ~( ( newValue >= 0.0 ) & ( newValue < 0.5 ) ) )
		errordlg( 'z-domain frequencies should be between 0.0 and 0.5 ...', ...
		                                                   'Input Out of Range', 'modal' );
		beep;
	else
		if strcmp( handles.approxMethod, 'vlach' )
			stopBandZeros = handles.stopBandZeros;
			if ( get( handles.checkbox_keepRatio, 'Value' ) == 1 )
				if ( handles.sDomain ~= 1 )
					stopBandZeros = lfSwitchDomain( stopBandZeros, 's' );
					stopBandZeros = stopBandZeros * newValue / handles.cutOffFrequency;
					stopBandZeros = lfSwitchDomain( stopBandZeros, 'z' );
				else
					stopBandZeros = stopBandZeros * newValue / handles.cutOffFrequency;
				end					
				handles.stopBandZeros = stopBandZeros; 
				set( handles.edit_stopBandZeros, 'String', num2str( stopBandZeros ) );
				handles.cutOffFrequency = newValue;
			else
				if any( stopBandZeros <= newValue )
		errordlg( 'Cutoff frequency should be lower than stopband zero frequencies ...', ...
														 'Cutoff Frequency Error', 'modal' );
					beep;
				else
					handles.cutOffFrequency = newValue;
				end
			end
		else
			handles.cutOffFrequency = newValue;
		end
	end
	set( handles.edit_cutOffFrequency, 'String', lfFormattedString(handles.cutOffFrequency) );
	guidata( hObject, handles );			% store the changes if any


% --- Executes on button press in checkbox_keepRatio.
function checkbox_keepRatio_Callback(hObject, eventdata, handles)
	% no action really


% --- Executes during object creation, after setting all properties.
function edit_stopBandZeros_CreateFcn(hObject, eventdata, handles)
	if ispc
    	set( hObject, 'BackgroundColor','white');
	else
    	set( hObject, 'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
	end

function edit_stopBandZeros_Callback(hObject, eventdata, handles)
	newValue = str2num(get( hObject, 'String'));
	if any( newValue <= handles.cutOffFrequency )
		errordlg( 'Not all stopband zero frequencies higher than cutoff frequency ...', ...
														 'Stopband Zeros Error', 'modal' );
		beep;
	elseif ( ( handles.sDomain == 0 )  & ~( all( newValue >= 0.0 ) & all( newValue < 0.5 ) ) )
		errordlg( 'All z-domain frequencies should be between 0.0 and 0.5 ...', ...
		                                                   'Input Out of Range', 'modal' );
		beep;
	else	                                                  
		handles.stopBandZeros = newValue;
		nStopBandZeros = length( newValue );
		nPossibleStopBandZeros = floor( handles.filterOrder / 2 );
		handles.stopBandZerosVector = [ ones(1,nStopBandZeros) ...
										zeros(1,nPossibleStopBandZeros-nStopBandZeros) ];

		infoStr = num2str( handles.stopBandZerosVector );
		set( handles.edit_stopBandZerosVector, 'String', infoStr );										
		guidata( hObject, handles );			% store the changes
	end
	set( handles.edit_stopBandZeros, 'String', lfFormattedString(handles.stopBandZeros) );



% --- Executes during object creation, after setting all properties.
function edit_stopBandZerosVector_CreateFcn(hObject, eventdata, handles)
	if ispc
    	set( hObject, 'BackgroundColor','white');
	else
    	set( hObject, 'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
	end

function edit_stopBandZerosVector_Callback(hObject, eventdata, handles)
	sBZVec = str2num( get( hObject, 'String' ) );
	nLocationsSpecified    = length( sBZVec );
	nPossibleStopBandZeros = floor( handles.filterOrder / 2 );
	nStopBandZeros         = length( handles.stopBandZeros );
	result = 1;
	if ( sum( sBZVec == 0 ) + sum( sBZVec == 1 ) ~= nLocationsSpecified )
		errorStr = 'Locations vector should contain only 0''s and/or 1''s ...';
		result = 0;
	end
	if ( result & ( nLocationsSpecified ~= nPossibleStopBandZeros ) )
		errorStr = sprintf( 'For this filterorder, %d locations are needed ...', ...
													nPossibleStopBandZeros ); 
		result = 0;
	end
	if ( result & ( sum( sBZVec == 1 ) ~= nStopBandZeros ) )
		errorStr = sprintf( '%d  1''s and %d 0''s expected ...', ...
						nStopBandZeros, nPossibleStopBandZeros-nStopBandZeros ); 
		result = 0;
	end
	if ~result
		errordlg( errorStr, 'Stopband Zero Locations Error', 'modal' );  
		beep;
		sBZVec = [];
	end								 		
	handles.stopBandZerosVector = sBZVec;
	infoStr = num2str( handles.stopBandZerosVector );
	set( handles.edit_stopBandZerosVector, 'String', infoStr );										
	guidata( hObject, handles );			% store the changes



% --- Executes during object creation, after setting all properties.
function edit_nUnitElements_CreateFcn(hObject, eventdata, handles)
	if ispc
    	set( hObject, 'BackgroundColor','white');
	else
    	set( hObject, 'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
	end


function edit_nUnitElements_Callback(hObject, eventdata, handles)
	% use str2num, because string can be empty
	handles.nUnitElements = str2num( get( hObject, 'String' ) );
	if isempty( handles.nUnitElements )
		handles.nUnitElements = 0;
	end
	handles.unitElementsVector = ones( 1, handles.nUnitElements );
	set( handles.edit_unitElementsVector, 'String', int2str(handles.unitElementsVector) );
	guidata( hObject, handles );			% store the changes



function edit_unitElementsVector_CreateFcn(hObject, eventdata, handles)
	if ispc
    	set( hObject, 'BackgroundColor','white');
	else
    	set( hObject, 'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
	end

function edit_unitElementsVector_Callback(hObject, eventdata, handles)
	handles.unitElementsVector = str2num(get( hObject, 'String'));
	handles.nUnitElements = sum( handles.unitElementsVector );
	set( handles.edit_nUnitElements, 'String', int2str(handles.nUnitElements) );
	guidata( hObject, handles );			% store the changes



function radiobutton_LowPass_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_LowPass, 'Value' ) == 0 )
		set( handles.radiobutton_LowPass, 'Value', 1 );
	else
		off = [ handles.radiobutton_HighPass, handles.radiobutton_BandPass, ...
												handles.radiobutton_BandStop ];
		lfMutualExclude( off );
		handles.filterType = 'lp';
		guidata( hObject, handles );			% store the changes
		set( handles.edit_centerFrequency, 'Visible', 'off' );
		set( handles.edit_bandWidth',      'Visible', 'off' );
	end


function radiobutton_HighPass_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_HighPass, 'Value' ) == 0 )
		set( handles.radiobutton_HighPass, 'Value', 1 );
	else
		off = [ handles.radiobutton_LowPass, handles.radiobutton_BandPass, ...
												handles.radiobutton_BandStop ];
		lfMutualExclude( off );
		handles.filterType = 'hp';
		guidata( hObject, handles );			% store the changes
		set( handles.edit_centerFrequency, 'Visible', 'off' );
		set( handles.edit_bandWidth',      'Visible', 'off' );
	end


function radiobutton_BandPass_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_BandPass, 'Value' ) == 0 )
		set( handles.radiobutton_BandPass, 'Value', 1 );
	else
		off = [ handles.radiobutton_LowPass, handles.radiobutton_HighPass, ...
												handles.radiobutton_BandStop ];
		lfMutualExclude( off );
		handles.filterType = 'bp';
		guidata( hObject, handles );			% store the changes
		set( handles.edit_centerFrequency, 'Visible', 'on' );
		set( handles.edit_bandWidth',      'Visible', 'on' );
	end


function radiobutton_BandStop_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_BandStop, 'Value' ) == 0 )
		set( handles.radiobutton_BandStop, 'Value', 1 );
	else
		off = [ handles.radiobutton_LowPass, handles.radiobutton_HighPass, ...
												handles.radiobutton_BandPass ];
		lfMutualExclude( off );
		handles.filterType = 'bs';
		guidata( hObject, handles );			% store the changes
		set( handles.edit_centerFrequency, 'Visible', 'on' );
		set( handles.edit_bandWidth',      'Visible', 'on' );
	end



% --- Executes during object creation, after setting all properties.
function edit_centerFrequency_CreateFcn(hObject, eventdata, handles)
  if ispc
      set( hObject, 'BackgroundColor','white');
  else
      set( hObject, 'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
  end


function edit_centerFrequency_Callback(hObject, eventdata, handles)
	newValue = str2double(get( hObject, 'String'));
	if ( ( handles.sDomain == 0 )  & ~( ( newValue >= 0.0 ) & ( newValue < 0.5 ) ) )
		errordlg( 'z-domain frequencies should be between 0.0 and 0.5 ...', ...
		                                                   'Input Out of Range', 'modal' );
		beep;
	else	                                                  
		handles.centerFrequency = newValue;
		guidata( hObject, handles );			% store the changes
	end
	set( handles.edit_centerFrequency, 'String', lfFormattedString(handles.centerFrequency) );



% --- Executes during object creation, after setting all properties.
function edit_bandWidth_CreateFcn(hObject, eventdata, handles)
  if ispc
      set( hObject, 'BackgroundColor','white');
  else
      set( hObject, 'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
  end


function edit_bandWidth_Callback(hObject, eventdata, handles)
	newValue = str2double(get( hObject, 'String'));
	if ( ( handles.sDomain == 0 )  & ~( ( newValue >= 0.0 ) & ( newValue < 0.5 ) ) )
		errordlg( 'z-domain frequencies should be between 0.0 and 0.5 ...', ...
		                                                   'Input Out of Range', 'modal' );
		beep;
	else	                                                  
		handles.bandWidth = newValue;
		guidata( hObject, handles );			% store the changes
	end
	set( handles.edit_bandWidth, 'String', lfFormattedString(handles.bandWidth) );



% --- Executes on button press in checkbox_Hs.
function checkbox_Hs_Callback(hObject, eventdata, handles)


% --- Executes on button press in checkbox_Hz.
function checkbox_Hz_Callback(hObject, eventdata, handles)


% --- Executes on button press in checkbox_ladderNetwork.
function checkbox_ladderNetwork_Callback(hObject, eventdata, handles)
	if ( get( handles.checkbox_ladderNetwork, 'Value' ) == 1 )
		if strcmp( handles.approxMethod, 'vlach' )
			set( handles.edit_stopBandZerosVector, 'Visible', 'on'  );
			set( handles.edit_unitElementsVector,  'Visible', 'on'  );
		end
		set( handles.radiobutton_serialFirst, 'Visible', 'on' );
		set( handles.radiobutton_shuntFirst,  'Visible', 'on' );
	else
		if ~( get( handles.checkbox_3pWDF, 'Value' ) == 1 )
			set( handles.edit_stopBandZerosVector, 'Visible', 'off' );
			set( handles.edit_unitElementsVector,  'Visible', 'off' );
			set( handles.radiobutton_serialFirst,  'Visible', 'off' );
			set( handles.radiobutton_shuntFirst,   'Visible', 'off' );
		end
	end

	
% --- Executes on button press in radiobutton_serialFirst.
function radiobutton_serialFirst_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_serialFirst, 'Value' ) == 0 )
		set( handles.radiobutton_serialFirst, 'Value', 1 );
	else
		set( handles.radiobutton_shuntFirst, 'Value', 0 );
	end


function radiobutton_shuntFirst_Callback(hObject, eventdata, handles)
	% don't switch off by pushing own button
	if ( get( handles.radiobutton_shuntFirst, 'Value' ) == 0 )
		set( handles.radiobutton_shuntFirst, 'Value', 1 );
	else
		set( handles.radiobutton_serialFirst, 'Value', 0 );
	end


% --- Executes on button press in checkbox_LWDF.
function checkbox_LWDF_Callback(hObject, eventdata, handles)


% --- Executes on button press in checkbox_3pWDF.
function checkbox_3pWDF_Callback(hObject, eventdata, handles)
	if ( get( handles.checkbox_3pWDF, 'Value' ) == 1 )
		if strcmp( handles.approxMethod, 'vlach' )
			set( handles.edit_stopBandZerosVector, 'Visible', 'on'  );
			set( handles.edit_unitElementsVector,  'Visible', 'on'  );
		end
		set( handles.radiobutton_serialFirst, 'Visible', 'on');
		set( handles.radiobutton_shuntFirst,  'Visible', 'on');
		set( handles.checkbox_use2ports,      'Visible', 'on');
		orderX2 = ( strcmp(handles.filterType,'bp') || strcmp(handles.filterType,'bs') );
		if ( ~orderX2 && (rem(handles.filterOrder,2) == 1) )
			set( handles.checkbox_useSym,     'Visible', 'on');
		end		
	else
		if ~( get( handles.checkbox_ladderNetwork, 'Value' ) == 1 )
			set( handles.edit_stopBandZerosVector, 'Visible', 'off' );
			set( handles.edit_unitElementsVector,  'Visible', 'off' );
			set( handles.radiobutton_serialFirst,  'Visible', 'off');
			set( handles.radiobutton_shuntFirst,   'Visible', 'off');
		end
		set( handles.checkbox_use2ports, 'Visible', 'off');
		set( handles.checkbox_useSym,    'Visible', 'off');
	end


function checkbox_use2ports_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox_use2ports (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get( hObject, 'Value' ) returns toggle state of checkbox_use2ports


% --- Executes on button press in checkbox_useSym.
function checkbox_useSym_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox_useSym (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkbox_useSym


% --- Executes on button press in pushbutton_Apply.
function pushbutton_Apply_Callback(hObject, eventdata, handles)

	% first check that all necassary parameters are specified
	result = 1;
	missingParameters = 0;
	filterType   = handles.filterType;
	approxMethod = handles.approxMethod;
	filterOrder  = handles.filterOrder;
	sDomain      = handles.sDomain;
	if isempty( filterOrder )
		errordlg( 'Should specify at least a filter Order ...', 'Missing Input', 'modal' );
		missingParameters = 1;
	else
		cutOffFrequency   = handles.cutOffFrequency;
		if ( sDomain == 0 )
			cutOffFrequency = lfSwitchDomain( cutOffFrequency, 's' );
		end
		passBandRipple_dB = handles.passBandRipple_dB;
		stopBandRipple_dB = handles.stopBandRipple_dB;
		freqNormMode      = handles.freqNormMode;
		switch approxMethod
			case 'cheby'
				if isempty( passBandRipple_dB )
					errordlg( 'Should specify a passband ripple ...', 'Missing Input', 'modal' );
					missingParameters = 1;
				end
			case 'invcheby'
				if isempty( stopBandRipple_dB )
					errordlg( 'Should specify stopband info ...', 'Missing Input', 'modal' );
					missingParameters = 1;
				end
			case 'cauer'
				if ( isempty( passBandRipple_dB ) & ( cutOffFrequency == 1.0 ) & ...
						( strcmp(filterType,'lp') | strcmp(filterType,'hp') ) & ...
												get( handles.checkbox_LWDF, 'Value' ) == 1 )
					approxMethod = 'cauer_birec';
				elseif isempty( passBandRipple_dB )
					errordlg( 'Should specify a passband ripple ...', 'Missing Input', 'modal' );
					missingParameters = 1;
				end
				if ( ~missingParameters & isempty( stopBandRipple_dB ) )
					errordlg( 'Should specify stopband info ...', 'Missing Input', 'modal' );
					missingParameters = 1;
				end
				if ~missingParameters
					skwirMode = handles.skwirMode;
					ladderNetwork = ( get( handles.checkbox_ladderNetwork, 'Value' ) == 1 | ...
										 get( handles.checkbox_3pWDF, 'Value' ) == 1 );
					if ( ladderNetwork & xor( rem(filterOrder,2) == 1, skwirMode == 'A' ) )
						errorMsg = { 'When to be realized with lumped elements,' ;
									 'only odd order filters of type ''A'', or';
									 'even order filters of type ''B'' or ''C'' allowed ...' };
						errordlg( errorMsg, 'Parameter''s Mismatch', 'modal' );
						missingParameters = 1;
					end
				end
			case 'vlach'
				if isempty( passBandRipple_dB )
					errordlg( 'Should specify a passband ripple ...', 'Missing Input', 'modal' );
					missingParameters = 1;
				elseif ( length(handles.stopBandZeros) > filterOrder/2 )
					errordlg( 'Too many stopBandZeros for given filterOrder ...', ...
														'Parameter''s Mismatch', 'modal' );
					missingParameters = 1;
				elseif ( ~strcmp( filterType, 'lp' ) & ( handles.nUnitElements ~= 0 ) )
					errordlg( 'Unit Elements only allowed in Low Pass Filters ...', ...
														'Parameter''s Mismatch', 'modal' );
					missingParameters = 1;
				end
		end
		if ( ~missingParameters & ( (filterType == 'bp') | (filterType == 'bs') ) )
			centerFrequency = handles.centerFrequency;
			bandWidth       = handles.bandWidth;
			if isempty( centerFrequency )
				errordlg( 'Should specify the centerfrequency ...', 'Missing Input', 'modal' );
				missingParameters = 1;
			end
			if ( ~ missingParameters & isempty( bandWidth ) )
				errordlg( 'Should specify a bandwidth ...', 'Missing Input', 'modal' );
				missingParameters = 1;
			end
		end
	end
	if ~missingParameters
		if ( strcmp(filterType,'lp') | strcmp(approxMethod,'cauer_birec') )
			switch approxMethod
				case 'butter'
					Hs = Hs_butter(filterOrder,cutOffFrequency);
				case 'cheby'
					Hs = Hs_cheby(filterOrder,passBandRipple_dB,cutOffFrequency,freqNormMode);
				case 'invcheby'
					Hs = Hs_invcheby(filterOrder,stopBandRipple_dB,cutOffFrequency,freqNormMode);
				case 'cauer'
					[Hs,wp] = Hs_cauer(filterOrder,passBandRipple_dB,stopBandRipple_dB, ...
													skwirMode, cutOffFrequency,freqNormMode);
				case 'cauer_birec'
					[Hs,passBandRipple_dB,errorMsg] = Hs_cauer_birec(filterOrder, ...
																				stopBandRipple_dB, 0);
					result = isempty( errorMsg );
					if result;
						handles.passBandRipple_dB = passBandRipple_dB;
						set( handles.edit_passBandRipple_dB, 'String', num2str(passBandRipple_dB) );
						approxMethod = 'cauer';
						guidata( hObject, handles );			% store the changes
					else
 						errordlg( errorMsg, 'Cauer Bireciprocal Design Error', 'modal' );
 						beep;
					end
				case 'vlach'
					stopBandZeros = handles.stopBandZeros;
					if ( sDomain == 0 )
						stopBandZeros = lfSwitchDomain( stopBandZeros, 's' );
					end
					nUnitElements = handles.nUnitElements;
					[Hs,wp] = Hs_vlach(filterOrder,passBandRipple_dB,cutOffFrequency, ...
												stopBandZeros,nUnitElements,freqNormMode);
			end
			HsLP = Hs;
		else
			switch approxMethod
				case 'butter'
					Hs = Hs_butter(filterOrder,1.0);
				case 'cheby'
					Hs = Hs_cheby(filterOrder,passBandRipple_dB,1.0,freqNormMode);
				case 'invcheby'
					Hs = Hs_invcheby(filterOrder,stopBandRipple_dB,1.0,freqNormMode);
				case 'cauer'
					[Hs,wp] = Hs_cauer(filterOrder,passBandRipple_dB,stopBandRipple_dB, ...
																skwirMode, 1.0,freqNormMode);
				case 'vlach'
					stopBandZeros = handles.stopBandZeros;
					if ( sDomain == 0 )
						stopBandZeros = lfSwitchDomain( stopBandZeros, 's' );
					end
					nUnitElements = handles.nUnitElements;
					[Hs,wp] = Hs_vlach(filterOrder,passBandRipple_dB,cutOffFrequency, ...
												stopBandZeros,nUnitElements,freqNormMode);
			end
			HsLP = Hs;
			switch filterType
				case 'hp'
					if ~strcmp(approxMethod,'vlach')
						Hs = nlp2hp( Hs, cutOffFrequency );
					else
						Hs = nlp2hp( Hs, cutOffFrequency^2 );
					end
				case 'bp'
					if ( sDomain == 0 )
						centerFrequency = lfSwitchDomain( centerFrequency, 's' );
						bandWidth       = lfSwitchDomain( bandWidth, 's' );
					end
					if ~strcmp(approxMethod,'vlach')
						Hs = nlp2bp( Hs, centerFrequency, bandWidth );
					else
						Hs = nlp2bp( Hs, centerFrequency, bandWidth/cutOffFrequency );
					end
				case 'bs'
					if ( sDomain == 0 )
						centerFrequency = lfSwitchDomain( centerFrequency, 's' );
						bandWidth       = lfSwitchDomain( bandWidth, 's' );
					end
					if ~strcmp(approxMethod,'vlach')
						Hs = nlp2bs( Hs, centerFrequency, bandWidth );
					else
						Hs = nlp2bs( Hs, centerFrequency, bandWidth*cutOffFrequency );
					end
			end
		end
%====
		if ( get( handles.checkbox_Hs, 'Value' ) == 1 )
			plotHs( Hs, 1, 1 );
			handles.figHsShown = 1;
			assignin( 'base', 'Hs_GUI', Hs );
		elseif ( handles.figHsShown ~= 0 )
			close( figure(1) );
			handles.figHsShown = 0;
		end
%====
		if ( get( handles.checkbox_Hz, 'Value' ) == 1 )
			Hz = Hs2Hz( Hs );
			plotHz( Hz, 1, 2 );
			handles.figHzShown = 1;
			assignin( 'base', 'Hz_GUI', Hz );
		elseif ( handles.figHzShown ~= 0 )
			close( figure(2) );
			handles.figHzShown = 0;
		end
%====
		ladderChecked = ( get( handles.checkbox_ladderNetwork, 'Value' ) == 1 );
		WDF_Checked   = ( get( handles.checkbox_3pWDF, 'Value' ) == 1 );
		if ( ladderChecked | WDF_Checked )
%====	start ladder network 	===============================================
			result = 1;
			SerialFirst = ( get( handles.radiobutton_serialFirst, 'Value' ) == 1 );
			switch approxMethod
				case 'butter'
					% determine topology
					elementsStr = char( 'C' * ones(1,filterOrder) );
					if SerialFirst
						elementsStr(1:2:end) = 'l';   % character 'el'
					else
						elementsStr(2:2:end) = 'l';   
					end
					Ladder.elements = [ 'r' elementsStr 'R' ];		
					% Now from:
					%	'explicit formula for a double-resistance-terminated lossless ladder'
					%	Active and Passive Analog Filter Design, An Introduction
					%	Lawrence P. Huelsman,  McGraw-Hill, Inc.;  1993
					%	ISBN 0-07-030860-8
					elValues = 2*sin( (1:2:2*filterOrder)*pi/(2*filterOrder) );
					% Source and Load resistors of 1 Ohm are assumed
					% Use column notation
					Ladder.values    = [ 1.0; elValues(:) / cutOffFrequency; 1.0 ];	
					figureNameString = 'Butterworth Low Pass Ladder Network';	
				case 'cheby'
					% determine topology
					elementsStr = char( 'C' * ones(1,filterOrder) );
					if SerialFirst
						elementsStr(1:2:end) = 'l';   % character 'el'
					else
						elementsStr(2:2:end) = 'l';   
					end
					Ladder.elements = [ 'r' elementsStr 'R' ];		
					[elValues,Rload] = lfChebyLC( filterOrder, passBandRipple_dB, freqNormMode );
					% NOTE: these elValue's and Rload hold true for a serial_first topology
					if ( get( handles.radiobutton_shuntFirst, 'Value' ) == 1 )
						Rload = 1/Rload;
					end
					Ladder.values    = [ 1.0; elValues(:) / cutOffFrequency; Rload ];		
					figureNameString = 'Chebyshev Low Pass Ladder Network';	
				case 'invcheby'
					roots_fs = HsLP.roots_fs;
					poly_gs  = HsLP.poly_gs;
					% reflection frequencies all at zero frequency
					%
					%                 g(s) + h(s)
					% construct Zi = -------------, while h(s) == g(s)[1] == 1
					%                 g(s) - h(s)
					%
					inputYZ.num = [ 2*poly_gs(1); poly_gs(2:end)' ];
					inputYZ.den = poly_gs(2:end)';
					% first, setup topology accounting for the resonators
					elType = [char('x'*ones(1,filterOrder)) 'R'];
					elType(2:2:end-1) = 'W';
					topology.elTypeStr = elType;
					% then, determine whether a type is to be extracted from a Z or a Y 
					topology.ZorYStr  = lfCreateZYstring(filterOrder,SerialFirst);
					ws       = imag( roots_fs(2:2:end) );
					nWs      = length(ws);
					wsIndex  = perms(1:nWs);   % (nWs:-1:1)
					nIndex   = size(wsIndex,1);
					nEls     = length(elType);
					elValues = zeros( 1 + nEls + floor((nEls-1)/2), nIndex );
					for i = 1:nIndex
						[elValues(:,i),result] = ladderSynthesis( inputYZ, topology, ...
																		ws(wsIndex(i,:)) );
					end
					if result
						Ladder.elements  = lfCodeElements(elType,topology.ZorYStr);
						Ladder.values    = elValues;
						figureNameString = 'Inverse-Chebyshev Low Pass Ladder Network';	
					end
				case 'cauer'
					% ... extract the necessary information from Hs 
					roots_fs = HsLP.roots_fs;
					poly_gs  = HsLP.poly_gs;
					% reconstruct h(s) in order to compute the input impedance/admittance
					poly_hs = poly([ j*wp; -j*wp]);
					% for odd filterOrders, there should be only a single pole at f_zero,
					% so strip off the last zero of poly_hs
					if ( skwirMode == 'A' )
						poly_hs = poly_hs(1:end-1);
					end
					inputYZ.num = ( poly_gs + poly_hs )';
					inputYZ.den = ( poly_gs - poly_hs )';
					inputYZ.den = inputYZ.den(2:end);
					% first, setup topology accounting for the resonators
					elType = [ char('x'*ones(1,filterOrder)) 'R' ];
					if ( skwirMode == 'A' )
						elType(2:2:end-1) = 'W';
					else
						elType(2:2:end-2) = 'W';
					end
					topology.elTypeStr = elType;
					% then, determine whether a type is to be extracted from a Z or a Y 
					topology.ZorYStr  = lfCreateZYstring(filterOrder,SerialFirst);
					ws       = imag( roots_fs(2:2:end) );
					nWs      = length(ws);
					wsIndex  = perms(1:nWs);   % (nWs:-1:1)
					nIndex   = size(wsIndex,1);
					elValues = zeros( 1 + length(elType) + nWs, nIndex );
					for i = 1:nIndex
						[elValues(:,i),result] = ladderSynthesis( inputYZ, topology, ...
																		ws(wsIndex(i,:)) );
					end
					if result
						Ladder.elements  = lfCodeElements(elType,topology.ZorYStr);
						Ladder.values    = elValues;
						figureNameString = 'Cauer Low Pass Ladder Network';	
					end
				case 'vlach'
					% ... extract the necessary information from Hs
					poly_fs = HsLP.poly_fs;
					if ( nUnitElements >= 1 )
						poly_fs = poly_fs{1};
					end 
					poly_gs = HsLP.poly_gs;
					% reconstruct h(s) in order to compute the input impedance/admittance
					poly_hs = poly([ j*wp; -j*wp]);
					% for odd filterOrders, there should be only a single pole at f_zero,
					% so strip off the last zero of poly_hs
					if ( rem(filterOrder + nUnitElements,2) == 1 )		% odd
						poly_hs = poly_hs(1:end-1);
					end
					if ( (filterOrder == 0) & (nUnitElements >= 1) )
						e = sqrt( 10^(passBandRipple_dB/10) -1 ); 
						C = sqrt(2)^nUnitElements / prod(1-wp.^2);
						poly_hs = e*C*poly_fs * poly_hs;
					end
					inputYZ.num = ( poly_gs + poly_hs )';
					denYZ       = ( poly_gs - poly_hs )';
					if ( abs(denYZ(1)) <= 1e-12 )		% not true if only UnitElements
						denYZ = denYZ(2:end);
					end
					inputYZ.den = denYZ;
					% first, setup topology accounting for stopBandZerosVec and unitElementsVec
					elType = [ char('x'*ones(1,filterOrder)) 'R' ];
					elType( 2*find( handles.stopBandZerosVector ) ) = 'W';
					for i = length(handles.unitElementsVector):-1:1
  		  	  			if ( handles.unitElementsVector(i) == 1 )
  		  	  				ipos = min(filterOrder+1,i);
    	        			elType = [ elType(1:ipos-1) 'U' elType(ipos:end) ];
  		  	  			end
					end
					topology.elTypeStr = elType;
					% then, determine whether a type is to be extracted from a Z or a Y 
					topology.ZorYStr  = lfCreateZYstring(filterOrder + nUnitElements, ...
																			SerialFirst);
					nStopBandZeros = length(stopBandZeros);
					sbzIndex = perms(1:nStopBandZeros);   % (nWs:-1:1)
					nIndex   = size(sbzIndex,1);
					elValues = zeros(filterOrder + nStopBandZeros + nUnitElements +2,nIndex);
					for i = 1:nIndex
						[elValues(:,i),result] = ladderSynthesis( inputYZ, topology, ...
															stopBandZeros(sbzIndex(i,:)) );
					end
					if result
						Ladder.elements  = lfCodeElements(elType,topology.ZorYStr);
						Ladder.values    = elValues;
						figureNameString = 'Vlach Low Pass Ladder Network';	
					end
			end
			if result
				switch filterType
					case 'hp'
						switch approxMethod
							case { 'invcheby', 'cauer' }
								Ladder = nladder2hp( Ladder, cutOffFrequency );
							otherwise
								Ladder = nladder2hp( Ladder, cutOffFrequency^2 );
						end
						figureNameString = strrep( figureNameString, 'Low', 'High' );	
					case 'bp'
						% if this code reached, centerFrequency and bandWidth already
						% in sDomain representation, due to calculations for Hs
						switch approxMethod
							case { 'invcheby', 'cauer' }
								Ladder = nladder2bp( Ladder, centerFrequency, bandWidth );
							otherwise
								Ladder = nladder2bp( Ladder, centerFrequency, ...
															bandWidth/cutOffFrequency );
						end
						figureNameString = strrep( figureNameString, 'Low', 'Band' );	
					case 'bs'
						switch approxMethod
							case { 'invcheby', 'cauer' }
								Ladder = nladder2bs( Ladder, centerFrequency, bandWidth );
							otherwise
								Ladder = nladder2bs( Ladder, centerFrequency, ...
															bandWidth*cutOffFrequency );
						end
						figureNameString = strrep( figureNameString, ...
															'Low Pass', 'Band Stop' );	
				end
%====	end ladder network 	===================================================
				if ladderChecked
					showLadder( Ladder, 3, figureNameString );
					ladder2Magn( Ladder, 1500, 4 );
					handles.figsLadderShown = 1;
					assignin( 'base', 'Ladder_GUI', Ladder );
				elseif ( handles.figsLadderShown ~= 0 )
					close( figure(3) );
					close( figure(4) );
					handles.figsLadderShown = 0;
				end
			else
				close( figure(3) );
				close( figure(4) );
				handles.figsLadderShown = 0;
				errordlg( 'Circuit not realizable within accuracy bounds ...', ...
													'Ladder circuit error', 'modal' );
				beep;
			end
		end
%====	start 3-port WDF 	===========================================
		if WDF_Checked
			if ( strcmp( approxMethod, 'vlach' ) & ( handles.nUnitElements ~= 0 ) )
				errordlg( 'Unit Elements not allowed with 3-port WDF''s ...', ...
												'3-port WDF Constraints Error', 'modal' );
				beep;
			else
				if ( get( handles.checkbox_use2ports, 'Value' ) ~= 1 )
					wdfTypeStr = '3p';
				else
					wdfTypeStr = '2p';
				end
				if ( get( handles.checkbox_useSym, 'Value' ) == 1 )
					wdfTypeStr = [ wdfTypeStr '_sym' ];
				end
				[WDF,fwdB,revB,allB] = ladder2WDF( Ladder, wdfTypeStr, 2048, 5 );
				handles.figsWDFShown = 1;
				assignin( 'base', 'WDF_GUI',  WDF  );
				assignin( 'base', 'fwdB_GUI', fwdB );
				assignin( 'base', 'revB_GUI', revB );
			end
		elseif ( handles.figsWDFShown ~= 0 )
			close( figure(5) );
			close( figure(6) );
			handles.figsWDFShown = 0;
		end
%====	end 3-port WDF 	===============================================
		if ( (result == 1) & ( get( handles.checkbox_LWDF, 'Value' ) == 1 ) )
		% be sure to pass always only one Hs (bireciprocal cauer !) 
			[LWDF,Hz_LWDF,Messages] = Hs2LWDF( Hs(1), 0, 0 );	
			if isempty(Messages.error)
				fprintf( Messages.warning );
				showLWDF( LWDF, 'L', 7 );
				plotHz( Hz_LWDF, 1,8, 0,2000, ...
							'Transfer Function reconstructed from LWDF Coefficients', ...
											[ ' forward B_{fwd}'; ' reverse B_{rev}' ] );
				axis( [ xlim -80 10 ] );											
				handles.figsLWDFShown = 1;
				assignin( 'base', 'LWDF_GUI', LWDF );
				assignin( 'base', 'Hz_LWDF_GUI', Hz_LWDF );
			else
				errordlg( Messages.error, 'LWDF Constraints Error', 'modal' );
				beep;
			end			
		elseif ( handles.figsLWDFShown ~= 0 )
			close( figure(7) );
			close( figure(8) );
			handles.figsLWDFShown = 0;
		end
		
		fprintf( '\n\n=====================================================\n\n' );
		
	else	% there are missingParameters
		beep;
	end		% test on missingParameters
	guidata( hObject, handles );		% update figShown handles


% --- Executes on button press in pushbutton_quit.
function pushbutton_quit_Callback(hObject, eventdata, handles)
	% Get the current position of the GUI from the handles structure
	% to pass to the modal dialog.
	pos_size = get(handles.figure1, 'Position' );
	% Call modaldlg with the argument 'Position'
	userResponse = modaldlg('Title','Confirm Quit');
	if strcmp( userResponse,'Yes' )
		delete(handles.figure1);
	end
	



%==========================================================================================
%=========  LOCAL FUNCTIONS  ======  LOCAL FUNCTIONS  ======  LOCAL FUNCTIONS  ============
%==========================================================================================

function lfMutualExclude( off )
  set(off, 'Value',0);


%==========================================================================================
function freq2 = lfSwitchDomain(freq1,newDomain)
  % Bilinear or Inverse bilinear frequency translation 
  %	fz = 0.25 corresponds with fs = 1.0
  if ( newDomain == 'z' )
	  freq2 = atan(freq1) / pi;
  else		% newDomain == 's'
	  freq2 = tan(freq1*pi);
  end

	
%==========================================================================================
function formattedStr = lfFormattedString(showValues)
	nValues = length( showValues );
	tmpStr  = [];
	for i = 1:nValues
		addStr = num2str( abs(showValues(i)), 5 );
		if isempty( find(addStr == '.') )
			addStr = [ addStr '.0' ];
		end
		if ( i ~= nValues )
			addStr = [ addStr '  ' ];
		end
		tmpStr = [ tmpStr addStr ];
	end
	formattedStr = tmpStr;	
	

%==========================================================================================
function zyStr = lfCreateZYstring(nElements,Z1)
  zyStr = char( 'Y' * ones(1,nElements+1) );
  if ( Z1 == 1 )
	  zyStr(1:2:end) = 'Z';
  else
	  zyStr(2:2:end) = 'Z';
  end


%==========================================================================================
function [LC,Rload] = lfChebyLC(filterOrder,passBandRipple_dB,freqNormMode)
  % Rsource is assumed to be 1 Ohm.
  %
  % See:	Wai-Kai Chen
  %   	John Wiley & Sons, Inc.
  %   	1986
  %   	ISBN 0-471-82352-X
  % where in the case that K == 1, aHat becomes 0 (Note that K ~= K@dc !!) 
  % For calculation of -3 dB frequency, see
  %   	Computerized Approximation and Synthesis of Lineair Networks
  %   	Jiri Vlach
  %   	pg. 256
  %
  % Note that always Rload == 1 for odd filterOrders.
  % For even filterOrders, when we start from a Zin (and the LC values are 
  % derived for that case), Rload == 2.65972 Ohm.
  % Starting from Yin then results in Rload == 0.37598  ( = 1/2.65972 )

  % implicit choice: Rsource = 1.0;
  k       = 10 ^ ( passBandRipple_dB/10 );
  epsilon = sqrt( k-1 );
  if ( rem(filterOrder,2) == 1 )	% odd order
	  Rload = 1;
  else								% even order
	  % the following choice of Rload implies that we start from a Zin
	  Rload = (2*k-1) + 2*sqrt( k*(k-1) );
  end

  a    = 1/filterOrder * asinh( 1/epsilon );
  tmp1 = ( sinh(a) )^2;
  phi  = ( 1:filterOrder ) * pi / filterOrder;
  fm   = ( (sinh(a))^2 )*ones(1,filterOrder) + ( sin(phi) ).^2;

  Q = [ 1/sinh(a);  zeros(filterOrder-1,1) ];	% column vector
  for i = 2:filterOrder
	  Q(i) = 1 / ( Q(i-1) * fm(i-1) );
  end
  LC = 2 * Q .* sin( (1:2:2*filterOrder)' * pi / (2*filterOrder) );

  if ( freqNormMode == 1)
	  LC = LC * cosh( 1/filterOrder * acosh(1/epsilon) );
  end


%==========================================================================================
function elString = lfCodeElements(elType,zyStr)
  %           resistor: 'r' or 'R',
  %           inductor: 'l' or 'L', 
  %          capacitor: 'c' or 'C',
  %   series resonator: 's' or 'S',
  % parallel resonator: 'p' or 'P',
  %       unit element: 'U'.
  % Lower case for series arms, upper case for shunt arms.
  elStr = char( ' ' * ones(1,length(elType)-1) );
  for i = 1:length(elType)-1
  	  switch elType(i)
  	  	  case 'x'
  	  	  	  if ( zyStr(i) == 'Z' )
  	  	  	  	 elStr(i) = 'l';
  	  	  	  else
  	  	  	  	 elStr(i) = 'C';
  	  	  	  end 
  	  	  case 'W'
  	  	  	  if ( zyStr(i) == 'Z' )
  	  	  	  	 elStr(i) = 'p';
  	  	  	  else
  	  	  	  	 elStr(i) = 'S';
  	  	  	  end 
  	  	  case 'U'
  	  	  	  elStr(i) = 'U';
	  end  	  	 
  end
  elString = [ 'r' elStr 'R' ];



